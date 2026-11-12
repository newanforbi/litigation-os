"""Matter 42 -- JS-CAND 44 civil cover sheet, Ngwa Nforbi v. Staples The Office
Superstore, LLC (N.D. Cal., San Jose). Fills the blank N.D. Cal. JS-CAND 44
form, stamps the canonical signature, and writes a fillable and a flattened
copy. Final, not yet filed (no case number).

    python3 internal/scripts/matter42-staples-civil-cover-sheet.py /path/to/blank-JS-CAND-44.pdf
"""
import os, sys
from pathlib import Path
import shutil, pymupdf as fz, pypdf
from pypdf.generic import NameObject, BooleanObject
SRC=sys.argv[1] if len(sys.argv) > 1 else sys.exit("usage: matter42-staples-civil-cover-sheet.py BLANK_JS_CAND_44.pdf")
OUT=os.environ.get("M42_OUT", "/tmp/m42-staples-complaint").rstrip("/")+"/"
os.makedirs(OUT, exist_ok=True)
FILLED=OUT+"Ngwa_Nforbi_v_Staples_Civil_Cover_Sheet_filled.pdf"
FLAT=OUT+"Ngwa_Nforbi_v_Staples_Civil_Cover_Sheet_flat.pdf"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from signature_stamp import SIGNATURE_ASPECT, SIGNATURE_PATH  # noqa: E402
SIG = SIGNATURE_PATH
DESC="No FCRA pre-adverse-action report copy/rights; CA ICRAA, PC 290.46(j), UCL"
TEXT={
 "Plaintiff":("Ngwa Nforbi, Brendan",10),
 "Defendant":("Staples The Office Superstore, LLC; and Does 1 through 25",10),
 "County_of_Residence_P1":("San Joaquin",10),
 "County_of_Residence_of_D1":("",10),
 "Plaintiff's Attorney(s)":("Brendan Ngwa Nforbi, Pro Se, 1455 Cat Tail Drive, Stockton, California 95204\n(209) 801-4442  |  brendan@ngwanforbi.com",8),
 "Defendant's Attorney(s) (If Known)":("Unknown",10),
 "Cause of Action":("15 U.S.C. § 1681 et seq. (FCRA), § 1681b(b)(3)(A)",9),
 "Description of case":(DESC,None),
 "Demand":("",10),
 "Related Case Information":("",10),
 "Today's Date":("October 21, 2026",10),
 "Signature of Attorney of Record":("",10),
}
# field name -> on-state to select
CHECK={"Group4":"Choice2",   # II. 3 Federal Question
       "Group5":"Choice54",  # IV. 480 Consumer Credit
       "V.Origin":"1",         # V. 1 Original Proceeding
       "Jury demand":"1", "$ Demand":"1",
       "Group3":"1"}         # IX. San Jose
doc=fz.open(SRC); pg=doc[0]
# description: largest Times size (<=8) that fits one line
dw=[w for w in pg.widgets() if w.field_name=="Description of case"][0]
avail=dw.rect.width-4
fs=min(8, avail/fz.get_text_length(DESC,"tiro",1)); fs=int(fs*10)/10
TEXT["Description of case"]=(DESC,fs)
seen=set()
for w in pg.widgets():
    n=w.field_name
    if n in TEXT:
        v,s=TEXT[n]; w.text_font="TiRo"; w.text_fontsize=s; w.field_value=v
        if n=="Signature of Attorney of Record": w.fill_color=None
        w.update(); seen.add(n)
missing=set(TEXT)-seen
assert not missing, missing
# signature stamp (canonical 445×106 wet-ink PNG), sitting on bottom of signature box
sw=[w for w in pg.widgets() if w.field_name=="Signature of Attorney of Record"][0].rect
width=108; h=width*SIGNATURE_ASPECT
r=fz.Rect(sw.x0+6, sw.y1-1-h, sw.x0+6+width, sw.y1-1)
pg.insert_image(r, filename=SIG, keep_proportion=False, overlay=True)
print("sig rect",r,"field",sw,"desc fs",fs)
doc.save(FILLED, garbage=3, deflate=True)
doc.close()
# NeedAppearances true in the fillable copy
rd=pypdf.PdfReader(FILLED); wr=pypdf.PdfWriter(clone_from=rd)
wr._root_object["/AcroForm"][NameObject("/NeedAppearances")]=BooleanObject(False)
# buttons: set /V and /AS directly, keeping the form's own appearance streams
done=set()
for a in wr.pages[0]["/Annots"]:
    a=a.get_object(); par=a.get("/Parent"); tgt=par.get_object() if par else a
    name=tgt.get("/T"); 
    if par is not None and par.get_object().get("/Parent") is not None:
        name=par.get_object()["/Parent"].get_object()["/T"]+"."+name
    if name not in CHECK: continue
    on=[k for k in a["/AP"]["/N"].keys() if k!="/Off"][0]
    if on=="/"+CHECK[name]:
        a[NameObject("/AS")]=NameObject(on); tgt[NameObject("/V")]=NameObject(on); done.add(name)
    else:
        a[NameObject("/AS")]=NameObject("/Off")
assert done==set(CHECK), set(CHECK)-done
# signature box: drop the gray /BG and give the empty field a transparent appearance
# so the stamped signature (page content) is not covered
from pypdf.generic import DictionaryObject, StreamObject, ArrayObject, FloatObject
for a in wr.pages[0]["/Annots"]:
    a=a.get_object()
    if a.get("/T")=="Signature of Attorney of Record":
        mk=a.get("/MK")
        if mk is not None and "/BG" in mk: del mk["/BG"]
        x0,y0,x1,y1=[float(v) for v in a["/Rect"]]
        st=StreamObject(); st.set_data(b"/Tx BMC EMC")
        st.update({NameObject("/Type"):NameObject("/XObject"),NameObject("/Subtype"):NameObject("/Form"),
                   NameObject("/BBox"):ArrayObject([FloatObject(0),FloatObject(0),FloatObject(x1-x0),FloatObject(y1-y0)])})
        a[NameObject("/AP")]=DictionaryObject({NameObject("/N"):wr._add_object(st)})
        print("signature widget BG removed")
wr.write(FILLED)
# flat
d=fz.open(FILLED); d.bake(annots=True, widgets=True); d.save(FLAT, garbage=3, deflate=True); d.close()
