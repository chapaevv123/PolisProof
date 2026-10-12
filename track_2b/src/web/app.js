const $=selector=>document.querySelector(selector);
const button=$('#compile'),upload=$('#upload'),download=$('#download'),caseSelect=$('#case-select');
let currentReceipt=null,currentPacket=null;
const escapeHtml=value=>String(value??'').replace(/[&<>'"]/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));
const highlight=text=>escapeHtml(text).replace(/(60[ .]000 EUR|40[ .]000 EUR|rechtlichen Prüfung|controllo legale|structural inspection)/gi,'<mark>$1</mark>');
const modeCopy={RECORDED_REPLAY:'Bundled synthetic cassette; no live request.',OFFLINE_FALLBACK:'Model unavailable; conservative local extraction.',LIVE_APERTUS:'Genuine configured Apertus endpoint.',ERROR:'Analysis did not complete.'};

async function loadPacket(name){
  const response=await fetch(`/api/packet/${encodeURIComponent(name)}`);
  if(!response.ok)throw new Error('Case could not be loaded');
  currentPacket=await response.json();
  renderSources(currentPacket.artifacts||[]);
  resetResults();
}
function renderSources(artifacts){
  $('#doc-count').textContent=`${artifacts.length} FILE${artifacts.length===1?'':'S'}`;
  $('#source-list').innerHTML=artifacts.map((item,index)=>`<div class="source ${index===0?'active':''}" tabindex="0"><div class="source-head"><b>${escapeHtml(item.title||item.artifact_id)}</b><span class="doc-meta"><span class="tag">${escapeHtml(item.language||'unknown')}</span><span class="tag ${escapeHtml(item.version||'')}">${escapeHtml(item.version||'source')}</span></span></div><p>${highlight(item.content)}</p></div>`).join('');
  document.querySelectorAll('.source').forEach(source=>source.addEventListener('click',()=>{document.querySelectorAll('.source').forEach(x=>x.classList.remove('active'));source.classList.add('active')}));
}
function resetResults(){
  currentReceipt=null;$('#claim-count').textContent='READY';$('#claim-list').className='empty-state';$('#claim-list').innerHTML='<span class="empty-icon">⌁</span><b>Ready to verify</b><p>Select a case and run the analysis.</p>';$('#status').className='verdict waiting';$('#status').innerHTML='<small>FINAL VERDICT</small><strong>WAITING</strong>';$('#reasons').innerHTML='';$('#truth').classList.add('hidden');$('#trace').classList.add('hidden');
}
function render(receipt){
  currentReceipt=receipt;const mode=receipt.execution_mode||'ERROR',status=receipt.verification_status||'ERROR',claims=receipt.claims||[];
  $('#mode-top').textContent=mode.replaceAll('_',' ');$('#execution').textContent=mode.replaceAll('_',' ');$('#mode-note').textContent=modeCopy[mode]||'Execution provenance recorded in receipt.';
  $('#status').className=`verdict ${status.toLowerCase()}`;$('#status').innerHTML=`<small>FINAL VERDICT</small><strong>${escapeHtml(status)}</strong>`;
  $('#reasons').innerHTML=(receipt.reason_codes||[]).map(code=>`<div class="reason">${escapeHtml(code.replaceAll('_',' '))}</div>`).join('');
  $('#claim-count').textContent=`${claims.length} CLAIM${claims.length===1?'':'S'}`;$('#claim-list').className='claim-list';
  $('#claim-list').innerHTML=claims.length?claims.map(claim=>{const state=(claim.verification_status||'').toLowerCase();return `<div class="claim ${state}"><div class="claim-top"><span>${escapeHtml(claim.claim_type)} · ${escapeHtml(claim.language)} · ${escapeHtml(claim.source_artifact)}</span><span class="claim-state ${state}">${escapeHtml(claim.verification_status)}</span></div><p>${escapeHtml(claim.statement)}</p><span class="evidence-quote">“${escapeHtml(claim.source_span)}”</span></div>`}).join(''):'<div class="empty-state"><b>No supported decision claim extracted.</b></div>';
  const routes=receipt.route||[],escalation=routes.find(item=>item.lane==='70B');$('#route').textContent=routes.map(item=>`Apertus ${item.lane}`).join(' → ')||'No model route';$('#routing').textContent=escalation?`Escalated because: ${String(escalation.reason||'disputed evidence').replaceAll('_',' ')}`:(mode==='OFFLINE_FALLBACK'?'Local deterministic fallback; no model called.':'No 70B escalation required.');
  $('#truth').classList.toggle('hidden',receipt.packet_id!=='demo_conflict');$('#trace').classList.remove('hidden');$('#hash').textContent=receipt.output_hash||'not issued';$('#trace').scrollIntoView({behavior:'smooth',block:'nearest'});
}
async function compile(url,options){
  button.disabled=true;button.querySelector('span').textContent='Analyzing…';
  try{const response=await fetch(url,options);const result=await response.json();if(!response.ok)throw new Error(result.error||'Analysis failed');render(result)}catch(error){render({execution_mode:'ERROR',verification_status:'ERROR',reason_codes:[error.message],claims:[],route:[]})}finally{button.disabled=false;button.querySelector('span').textContent='Run analysis'}
}
button.addEventListener('click',()=>compile(`/api/compile/${encodeURIComponent(caseSelect.value)}`));
caseSelect.addEventListener('change',()=>loadPacket(caseSelect.value).catch(error=>render({execution_mode:'ERROR',verification_status:'ERROR',reason_codes:[error.message],claims:[],route:[]})));
upload.addEventListener('change',async()=>{const file=upload.files[0];if(!file)return;const text=await file.text();let packet;if(file.name.toLowerCase().endsWith('.json')){try{packet=JSON.parse(text)}catch{packet=null}}if(!packet||!Array.isArray(packet.artifacts)){packet={packet_id:`upload-${Date.now()}`,title:'Uploaded text',artifacts:[{artifact_id:'uploaded-document',title:file.name,language:'unknown',version:'uploaded',content:text}]}}currentPacket=packet;renderSources(packet.artifacts);compile('/api/compile',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(packet)})});
download.addEventListener('click',()=>{if(!currentReceipt)return;const blob=new Blob([JSON.stringify(currentReceipt,null,2)],{type:'application/json'}),link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download=`polisproof-${currentReceipt.packet_id||'error'}-receipt.json`;link.click();setTimeout(()=>URL.revokeObjectURL(link.href),0)});
fetch('/api/health').then(r=>r.json()).then(health=>{$('#server-state').textContent=health.status==='ok'?'LOCAL SERVER READY':'SERVER ERROR'}).catch(()=>{$('#server-state').textContent='SERVER OFFLINE'});
loadPacket('demo_conflict').catch(error=>render({execution_mode:'ERROR',verification_status:'ERROR',reason_codes:[error.message],claims:[],route:[]}));
