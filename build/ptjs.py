import re,json,sys
sys.path.insert(0,'/home/claude/vdp')
from pt import PT
S='/home/claude/vdp/s65/'
MON={'Jan':'jan','Feb':'fev','Mar':'mar','Apr':'abr','May':'mai','Jun':'jun','Jul':'jul','Aug':'ago','Sep':'set','Oct':'out','Nov':'nov','Dec':'dez'}
def dates(s):
    s=re.sub(r'\b(\d{1,2}) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b',lambda m:m.group(1)+' '+MON[m.group(2)],s)
    s=re.sub(r'\bmid-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b',lambda m:'meados '+MON[m.group(1)],s)
    s=re.sub(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{4})\b',lambda m:MON[m.group(1)]+' '+m.group(2),s)
    return s
HJ={
'#32, 94 pts · James Suckling Top 100 Wines of Portugal.':'32.º, 94 pts · Top 100 Wines of Portugal de James Suckling.',
'1534–1537 · Paris to Rome':'1534–1537 · De Paris a Roma','1537–1540 · Rome':'1537–1540 · Roma','1540 · Two routes to Lisbon':'1540 · Dois caminhos para Lisboa','1551 · Évora':'1551 · Évora',
'1605 · Évora to Portalegre':'1605 · De Évora a Portalegre','1605–1759 · Reguengo':'1605–1759 · Reguengo','1759 · To the Crown':'1759 · Para a Coroa','1795 · Vinha dos Padres':'1795 · Vinha dos Padres',
'1876–1953 · The vines are planted':'1876–1953 · São plantadas as vinhas','1953–1980s · The original talha wines':'1953–anos 80 · Os vinhos de talha originais','1980s–2010 · Abandoned':'anos 80–2010 · Abandono',
'2010–2020 · A quiet decade':'2010–2020 · Uma década tranquila','2020 · A winemaking family returns':'2020 · Regressa uma família de vinhateiros','2022 · Rua do Saco and Quinta da Casquinha':'2022 · Rua do Saco e Quinta da Casquinha',
'2025 · Caldeiras':'2025 · Caldeiras','2026 · Fialha and Vinha da Broa':'2026 · Fialha e Vinha da Broa',
'António Trindade Crespo makes Quinta da Vinha dos Padres red and white.':'António Trindade Crespo faz o Quinta da Vinha dos Padres tinto e branco.',
'Both leave Rome together: Rodrigues by sea, Xavier overland through France and Madrid.':'Ambos partem de Roma: Rodrigues por mar, Xavier por terra através de França e Madrid.',
'College 1551':'Colégio 1551','College of the Holy Spirit; university from 1559.':'Colégio do Espírito Santo; universidade desde 1559.','First modern vintage, made in talhas at ~600 m.':'Primeira colheita moderna, feita em talhas a ~600 m.',
'Formula 1539':'Fórmula 1539','Formula of the Institute (1539); papal approval, 27 September 1540.':'Fórmula do Instituto (1539); aprovação papal, 27 de setembro de 1540.',
'Lisbon':'Lisboa','Montmartre · 15 Aug 1534':'Montmartre · 15 ago 1534','Only the centenary vines that survive today remain.':'Restam apenas as vinhas centenárias que hoje sobrevivem.',
'Papal bull 27 Sep 1540':'Bula papal 27 set 1540','Portalegre DOC':'DOC Portalegre','Reguengo parish under Jesuit cultivation.':'Freguesia do Reguengo cultivada pelos Jesuítas.',
'Reguengo, Portalegre · Alto Alentejo, Portugal':'Reguengo, Portalegre · Alto Alentejo, Portugal','Rome':'Roma','Serra de São Mamede Natural Park':'Parque Natural da Serra de São Mamede',
'Six properties around Reguengo. Click a property to explore it.':'Seis propriedades à volta do Reguengo. Clique numa propriedade para a explorar.',
'The Crown divides the estate; the Achioli family buys the collective parcel (estimated extent).':'A Coroa divide a propriedade; a família Achioli compra a parcela coletiva (extensão estimada).',
'The Jesuits are expelled from Portugal; their lands pass to the Crown.':'Os Jesuítas são expulsos de Portugal; as suas terras passam para a Coroa.',
'The Silveira Catemario di Quadri family; the parcels come back to life.':'A família Silveira Catemario di Quadri; as parcelas voltam à vida.',
'The first companions travel together to Venice and Rome.':'Os primeiros companheiros viajam juntos até Veneza e Roma.','The road to the College of São Sebastião.':'O caminho para o Colégio de São Sebastião.',
'University 1559':'Universidade 1559','Untended, the old vines decline.':'Sem cuidados, as vinhas velhas declinam.','Venice':'Veneza',
'c. 1876–1890 planting · 1931 register, c. 6,000 vines · Vila Maria, 1920s.':'plantação c. 1876–1890 · registo de 1931, c. 6000 videiras · Vila Maria, anos 20.',
'College of São Sebastião · 1605':'Colégio de São Sebastião · 1605',
}
def lit_replace(s,M,keyguard=True):
    def r(m):
        q,v=m.group(1),m.group(2)
        pre=s[max(0,m.start()-3):m.start()]
        if keyguard and pre.endswith('LN['): return m.group(0)
        if v in M: return q+M[v].replace(q,'\\'+q)+q
        return m.group(0)
    return re.sub(r"(')((?:[^'\\\n]|\\.)*)'",r,s)
# ---------- history-pt ----------
f=S+'history-pt.html'; h=open(f).read()
a=h.find('const STOP='); b=h.find('const ORDER=',a); b=b if b>0 else a+40000
seg=h[a:b]; seg=lit_replace(seg,HJ)
seg=re.sub(r"'([^'\n]*\b(?:\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}|mid-\w+)[^'\n]*)'",lambda m:"'"+dates(m.group(1))+"'",seg)
h=h[:a]+seg+h[b:]
i=h.find('const REG=['); j=h.find('];',i); h=h[:i]+lit_replace(h[i:j],HJ)+h[j:]
h=h.replace("'Quinta da Vinha dos Padres '+d.src.split('-').reverse().join(' ').replace('white','White').replace('red','Red')+' · see the wine'","'Quinta da Vinha dos Padres '+d.src.split('-').reverse().join(' ').replace('white','branco').replace('red','tinto')+' · ver o vinho'")
h=h.replace("['Quinta da','Vinha dos','Padres','1953–1980s']","['Quinta da','Vinha dos','Padres','1953–anos 80']")
open(f,'w').write(h)
# ---------- compare-pt ----------
f=S+'compare-pt.html'; h=open(f).read()
i=h.find('const CD='); j=h.find(';',h.find(',PJ=',i)) if ',PJ=' in h[i:i+400000] else h.find(';',h.find(',IC=',i))
CJ={'months skin contact (talha)':'meses de maceração (talha)','total months in talha':'meses totais em talha','months in used oak':'meses em carvalho usado','alcohol %':'álcool %','acidity g/L':'acidez g/L',
 'bottles':'garrafas','critics':'crítica','nose':'nariz','mouth':'boca','nose &amp; mouth':'nariz e boca','Same vines, same talhas, different choices.':'As mesmas vinhas, as mesmas talhas, escolhas diferentes.',
 'Same vines, same talhas: in 2023 the white left the talha after 3 months instead of 12.':'As mesmas vinhas, as mesmas talhas: em 2023 o branco saiu da talha ao fim de 3 meses em vez de 12.',
 'Same vines, same talhas: in 2023 the red left the talha after 3 months and spent 4 more in used oak.':'As mesmas vinhas, as mesmas talhas: em 2023 o tinto saiu da talha ao fim de 3 meses e estagiou mais 4 em carvalho usado.',
 'Much paler than the longer-aged 2022… more fruit and less of the dried grasses/hay aroma.':'Muito mais pálido do que o 2022, de estágio mais longo… mais fruta e menos aroma de erva seca/feno.',
 'The 2023… feels quite primary and fruit-driven compared to the 2022 I tasted next to it.':'O 2023… parece bastante primário e frutado, comparado com o 2022 que provei ao lado.',
 'golden yellow, amber reflection':'amarelo dourado, reflexo âmbar','deep ruby, bright':'rubi profundo, brilhante','paler, no orange':'mais pálido, sem laranja','golden yellow':'amarelo dourado',
 '2022 white':'2022 branco','2022 red':'2022 tinto','2023 white':'2023 branco','2023 red':'2023 tinto'}
# translate JSON-ish data strings (names, colours, pair texts)
def jrep(s):
    for k,v in CJ.items(): s=s.replace(': "'+k+'"',': "'+v+'"').replace('["'+k+'"','["'+v+'"').replace(', "'+k+'"]',', "'+v+'"]')
    return s
h=h[:i]+jrep(h[i:j])+h[j:]
k=h.find(';',j)  # script body after data
body_i=j; body_j=h.find('</script>',body_i)
sb=h[body_i:body_j]
for kk,vv in CJ.items(): sb=sb.replace("'"+kk+"'","'"+vv+"'")
sb=sb.replace('<h2 class="hd">nose &amp; mouth</h2>','<h2 class="hd">nariz e boca</h2>').replace("<h4>nose</h4>","<h4>nariz</h4>").replace("<h4>mouth</h4>","<h4>boca</h4>")
sb=sb.replace('<div class="hd">critics</div>','<div class="hd">crítica</div>')
TERMS={k:v for k,v in PT.items() if k.islower() or k in ('pH',)}
assert '<figcaption>${t}</figcaption>' in sb
sb=sb.replace('<figcaption>${t}</figcaption>','<figcaption>${TPT[t]||t}</figcaption>')

h=h[:body_i]+sb+h[body_j:]
assert h.count('<script>const CD=')==1
h=h.replace('<script>const CD=','<script>const TPT='+json.dumps(TERMS,ensure_ascii=False)+';const CD=',1)
open(f,'w').write(h)
# ---------- contact-pt ----------
f=S+'contact-pt.html'; h=open(f).read()
for a,b in [("'Sent ✓'","'Enviado ✓'"),("'Thank you. Your message has been sent; we will reply personally.'","'Obrigado. A sua mensagem foi enviada; responderemos pessoalmente.'"),("'Opening your email app to send the message…'","'A abrir a sua aplicação de email para enviar a mensagem…'"),("'Please fill in all required fields.'","'Preencha todos os campos obrigatórios.'")]:
    h=h.replace(a,b)
open(f,'w').write(h)
print('ok')
