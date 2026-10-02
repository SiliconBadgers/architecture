const T=['T',1,0];
function architecture(c){return {linearLayers:c.layer_types.filter(x=>x==='linear_attention').length,fullLayers:c.layer_types.filter(x=>x==='full_attention').length,keyDim:c.linear_key_head_dim,valueDim:c.linear_value_head_dim,valueHeads:c.linear_num_value_heads,convKernel:c.linear_conv_kernel_dim,convChannels:2*c.linear_key_head_dim*c.linear_num_key_heads+c.linear_value_head_dim*c.linear_num_value_heads,kvWidth:c.num_key_value_heads*c.head_dim};}
function graph(d){
 const c=d.text_config,H=c.hidden_size,I=c.intermediate_size,V=c.vocab_size,A=architecture(c),Q=c.num_attention_heads*c.head_dim,KV=A.kvWidth,R=A.valueDim*A.valueHeads;
 const tensors=[],order=[];let prefix='';
 function add(name,op,shape,src=[],weight=false){const id=tensors.length;tensors.push({id,name:prefix+name,op,shape:[...shape,...Array(4-shape.length).fill(1)],src,weight,view:-1,dtype:'f32'});if(op!=='NONE'&&op!=='VIEW'&&op!=='RESHAPE')order.push(id);return id;}
 const w=(n,k,m=1)=>add(n,'NONE',[k,m],[],true);
 const view=(n,x,shape)=>add(n,'RESHAPE',shape,[x]);
 const mm=(n,x,k,m,t=T)=>add(n,'MUL_MAT',[m,t],[w(n+'.weight',k,m),x]);
 const simple=(n,op,shape,src)=>add(n,op,shape,src);
 function norm(n,x,shape){const r=simple(n+'.rms','RMS_NORM',shape,[x]);return simple(n+'.scale','MUL',shape,[r,w(n+'.weight',shape[0])]);}
 const emb=w('token_embd.weight',H,V),ids=add('tokens','NONE',[T],[]);let x=add('embedding','GET_ROWS',[H,T],[emb,ids]);
 for(let l=0;l<c.num_hidden_layers;l++){
  prefix='blk.'+l+'.';const residual=x;let a=norm('attn_norm',x,[H,T]);
  if(c.layer_types[l]==='linear_attention'){
   const qkv=mm('qkv',a,H,A.convChannels),cw=w('conv.weight',A.convKernel,A.convChannels);
   const conv=simple('conv','SSM_CONV',[A.convChannels,T],[qkv,cw]);const silu=simple('conv_silu','SILU',[A.convChannels,T],[conv]);
   let q=view('q',silu,[A.keyDim,c.linear_num_key_heads,T]),k=view('k',silu,[A.keyDim,c.linear_num_key_heads,T]),v=view('v',silu,[A.valueDim,A.valueHeads,T]);
   q=simple('q_l2','RMS_NORM',[A.keyDim,c.linear_num_key_heads,T],[q]);k=simple('k_l2','RMS_NORM',[A.keyDim,c.linear_num_key_heads,T],[k]);
   // GatedDeltaNet expands key/query heads to value heads where needed.
   q=view('q_expanded',q,[A.keyDim,A.valueHeads,T]);k=view('k_expanded',k,[A.keyDim,A.valueHeads,T]);
   const alpha=mm('alpha',a,H,A.valueHeads),beta=mm('beta',a,H,A.valueHeads);
   const ap=simple('alpha_bias','ADD',[A.valueHeads,T],[alpha,w('dt.bias',A.valueHeads)]);
   const sp=simple('softplus','SOFTPLUS',[A.valueHeads,T],[ap]);const gate=simple('gate','MUL',[A.valueHeads,T],[sp,w('A_log',A.valueHeads)]);
   const bs=simple('beta_sigmoid','SIGMOID',[A.valueHeads,T],[beta]);const state=add('state','NONE',[A.keyDim,A.valueDim,A.valueHeads]);
   let out=simple('delta','GATED_DELTA_NET',[A.valueDim,A.valueHeads,T],[q,k,v,gate,bs,state]);
   out=norm('gdn_norm',out,[A.valueDim,A.valueHeads,T]);let z=mm('z',a,H,R);z=simple('z_silu','SILU',[R,T],[z]);
   out=view('delta_flat',out,[R,T]);out=simple('delta_gate','MUL',[R,T],[out,z]);a=mm('out',out,R,H);
  }else{
   const qgate=mm('q_gate',a,H,2*Q),q=view('q',qgate,[c.head_dim,c.num_attention_heads,T]);
   let qn=norm('q_norm',q,[c.head_dim,c.num_attention_heads,T]);qn=simple('q_rope','ROPE',[c.head_dim,c.num_attention_heads,T],[qn]);
   const k0=mm('k',a,H,KV),v0=mm('v',a,H,KV);let k=view('k_heads',k0,[c.head_dim,c.num_key_value_heads,T]);k=norm('k_norm',k,[c.head_dim,c.num_key_value_heads,T]);k=simple('k_rope','ROPE',[c.head_dim,c.num_key_value_heads,T],[k]);
   const ck=add('cache_k_','NONE',[c.head_dim,'K',c.num_key_value_heads]),cv=add('cache_v_','NONE',['K',c.head_dim,c.num_key_value_heads]);
   simple('store_k','SET_ROWS',[KV,T],[k,ck]);simple('store_v','SET_ROWS',[KV,T],[v0,cv]);
   const score=simple('scores','MUL_MAT',['K',T,c.num_attention_heads],[ck,qn]);const prob=simple('softmax','SOFT_MAX',['K',T,c.num_attention_heads],[score]);
   let out=simple('weighted_v','MUL_MAT',[c.head_dim,T,c.num_attention_heads],[cv,prob]);out=view('attention_flat',out,[Q,T]);
   let gate=view('output_gate',qgate,[Q,T]);gate=simple('output_sigmoid','SIGMOID',[Q,T],[gate]);out=simple('gated_output','MUL',[Q,T],[out,gate]);a=mm('out',out,Q,H);
  }
  x=simple('attention_residual','ADD',[H,T],[residual,a]);const residual2=x;x=norm('ffn_norm',x,[H,T]);
  const gate=mm('ffn_gate',x,H,I),up=mm('ffn_up',x,H,I);const act=simple('swiglu','SWIGLU',[I,T],[gate,up]);x=mm('ffn_down',act,I,H);x=simple('ffn_residual','ADD',[H,T],[residual2,x]);
 }
 prefix='';x=norm('final_norm',x,[H,T]);x=view('last_token',x,[H,1]);const outWeight=(c.tie_word_embeddings??d.tie_word_embeddings)?emb:w('output.weight',H,V);add('result_output','MUL_MAT',[V,1],[outWeight,x]);
 return {tensors,order,arch:A,model:'synthetic config-derived graph'};
}
function paramCount(d){
 const c=d.text_config,H=c.hidden_size,A=architecture(c),Q=c.num_attention_heads*c.head_dim,KV=A.kvWidth,R=A.valueDim*A.valueHeads;
 const tie=c.tie_word_embeddings??d.tie_word_embeddings;
 const linear=H*(A.convChannels+2*R+2*A.valueHeads)+A.convKernel*A.convChannels+2*A.valueHeads+A.valueDim;
 const full=H*(3*Q+2*KV)+2*c.head_dim;
 const mlp=c.num_experts?3*H*(c.num_experts*c.moe_intermediate_size+c.shared_expert_intermediate_size)+H*c.num_experts+H:3*H*c.intermediate_size;
 return H*c.vocab_size*(tie?1:2)+A.linearLayers*linear+A.fullLayers*full+c.num_hidden_layers*(mlp+2*H)+H;
}

module.exports={architecture,graph,paramCount};
