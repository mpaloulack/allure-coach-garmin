/* Recale les dates de l'exemple sur la semaine en cours (démo uniquement). */
(function(raw){
 const D=864e5,pad=n=>String(n).padStart(2,"0");
 const now=new Date(),today=new Date(now.getFullYear(),now.getMonth(),now.getDate(),12);
 const ex=raw._demo&&raw._demo.today?new Date(raw._demo.today+"T12:00:00"):today;
 const mon=x=>{const m=new Date(x);m.setDate(x.getDate()-((x.getDay()+6)%7));return m};
 const shift=Math.round((mon(today)-mon(ex))/(7*D))*7;
 const sh=s=>{const d=new Date(s+"T12:00:00");d.setDate(d.getDate()+shift);return d.getFullYear()+"-"+pad(d.getMonth()+1)+"-"+pad(d.getDate())};
 const isoRe=/^\d{4}-\d{2}-\d{2}$/;
 const walk=v=>Array.isArray(v)?v.map(walk):v&&typeof v==="object"?Object.fromEntries(Object.entries(v).map(([k,x])=>[k,walk(x)])):(typeof v==="string"&&isoRe.test(v))?sh(v):v;
 const out=walk(raw);delete out._demo;
 const dm=s=>{const [dd,mm]=s.split("/").map(Number);const d=new Date(ex.getFullYear(),mm-1,dd,12);d.setDate(d.getDate()+shift);return pad(d.getDate())+"/"+pad(d.getMonth()+1)};
 const sn=out.snapshot||{};["load","hrv","sleep"].forEach(k=>{if(sn[k])sn[k]=sn[k].map(r=>[dm(r[0])].concat(r.slice(1)))});
 sn.syncedAt=Date.now();
 const MO=["janv.","févr.","mars","avr.","mai","juin","juil.","août","sept.","oct.","nov.","déc."];
 (out.plan||[]).forEach(w=>{const m=mon(new Date(w.s[0].d+"T12:00:00")),e=new Date(m);e.setDate(m.getDate()+6);
  w.range=m.getMonth()===e.getMonth()?m.getDate()+"–"+e.getDate()+" "+MO[e.getMonth()]:m.getDate()+" "+MO[m.getMonth()]+"–"+e.getDate()+" "+MO[e.getMonth()]});
 return out})
