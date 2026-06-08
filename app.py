#!/usr/bin/env python3
"""Victim Advocate - AIIT Apps Division | AIIT Corporation 2026"""
from flask import Flask, request, make_response, redirect, jsonify
import importlib, os, io
from pricing_route import pricing_bp
from seed_resources import RESOURCES, STATES, CRIMES
from templates import page

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "va-dev")
app.register_blueprint(pricing_bp)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "app": "victim_advocate"}), 200

def load_rights():
    rights = {}
    mods = {"FL":"rights_fl","GA":"rights_ga","IL":"rights_il",
            "MI":"rights_mi","NC":"rights_nc","NY":"rights_ny",
            "OH":"rights_oh","PA":"rights_pa","TX":"rights_tx","OK":"rights_ok"}
    for code, mod in mods.items():
        try:
            m = importlib.import_module(mod)
            for r in m.DATA:
                rights[(r[0],r[1])] = dict(state=r[0],crime=r[1],
                    rights=r[2],sol=r[3],reporting=r[4],compensation=r[5])
        except Exception as e:
            print(f"Warning: {mod}: {e}")
    return rights

DB = load_rights()

def sel_opts(m, sel=""):
    o = ""
    for k,v in sorted(m.items(), key=lambda x:x[1]):
        s = " selected" if k==sel else ""
        o += '<option value="'+k+'"'+s+'>'+v+'</option>'
    return o

def search_form(ss="", sc=""):
    h = '<h2 class="mb-4">Know Your Rights</h2>'
    h += '<form method="POST" action="/rights"><div class="row">'
    h += '<div class="col-md-5 mb-3">'
    h += '<label class="form-label fw-bold">Your State</label>'
    h += '<select name="state" class="form-select form-select-lg" required>'
    h += '<option value="">Select state...</option>' + sel_opts(STATES, ss)
    h += '</select></div>'
    h += '<div class="col-md-5 mb-3">'
    h += '<label class="form-label fw-bold">Type of Crime</label>'
    h += '<select name="crime" class="form-select form-select-lg" required>'
    h += '<option value="">Select crime type...</option>' + sel_opts(CRIMES, sc)
    h += '</select></div>'
    h += '<div class="col-md-2 mb-3 d-flex align-items-end">'
    h += '<button type="submit" class="btn btn-primary btn-lg w-100">Search</button>'
    h += '</div></div></form>'
    return h

@app.route("/")
def home():
    b = '<div class="text-center py-5" style="background:linear-gradient(135deg,#2C1654,#6C3FA0);color:white;border-radius:12px;margin-bottom:30px;">'
    b += '<h1 class="display-4 fw-bold">You Are Not Alone</h1>'
    b += '<p class="lead mt-3">Know your rights. Find help. Take the next step.</p>'
    b += '<p>Free legal rights lookup for crime victims across 10 states</p>'
    b += '<div class="mt-4">'
    b += '<a href="/rights" class="btn btn-light btn-lg me-2">Know Your Rights</a>'
    b += '<a href="/resources" class="btn btn-outline-light btn-lg">Find Resources</a>'
    b += '</div></div>'
    b += '<div class="row text-center mt-4">'
    b += '<div class="col-md-4 mb-3"><div class="card p-4 h-100"><h3>Rights Lookup</h3>'
    b += '<p>Search victim rights by state and crime type.</p></div></div>'
    b += '<div class="col-md-4 mb-3"><div class="card p-4 h-100"><h3>Resources</h3>'
    b += '<p>National hotlines, crisis text lines, legal aid.</p></div></div>'
    b += '<div class="col-md-4 mb-3"><div class="card p-4 h-100"><h3>PDF Reports</h3>'
    b += '<p>Printable summary for your attorney or advocate.</p></div></div></div>'
    b += '<p class="text-center text-muted mt-3">In immediate danger? Call <strong>911</strong>.</p>'
    return page("Home", b)

@app.route("/rights", methods=["GET","POST"])
def rights():
    if request.method == "GET":
        return page("Know Your Rights", search_form())
    st = request.form.get("state","")
    cr = request.form.get("crime","")
    data = DB.get((st, cr))
    if not data:
        msg = '<div class="alert alert-warning mt-3">No data found.</div>'
        return page("Know Your Rights", search_form(st,cr)+msg)
    sn = STATES.get(st, st)
    cn = CRIMES.get(cr, cr)
    c = '<div class="card mt-4">'
    c += '<div class="card-header" style="background:linear-gradient(135deg,#2C1654,#6C3FA0);color:white;">'
    c += '<h4 class="mb-0">'+cn+' &mdash; '+sn+'</h4></div>'
    c += '<div class="card-body"><div class="row">'
    c += '<div class="col-md-6 mb-3"><h5>Your Rights</h5><p>'+data["rights"]+'</p></div>'
    c += '<div class="col-md-6 mb-3"><h5>Statute of Limitations</h5><p>'+data["sol"]+'</p></div>'
    c += '<div class="col-md-6 mb-3"><h5>Mandatory Reporting</h5><p>'+data["reporting"]+'</p></div>'
    c += '<div class="col-md-6 mb-3"><h5>Compensation</h5><p>'+data["compensation"]+'</p></div>'
    c += '</div><div class="text-center mt-3">'
    c += '<a href="/pdf?state='+st+'&crime='+cr+'" class="btn btn-secondary">Download PDF</a>'
    c += '</div></div></div>'
    return page(cn+" - "+sn, search_form(st,cr)+c)

@app.route("/resources")
def resources():
    cards = ""
    for name, phone, url, desc, rtype in RESOURCES:
        ph = '<p class="fw-bold">'+phone+'</p>' if phone else ""
        cards += '<div class="col-md-6 mb-3"><div class="card p-3 h-100">'
        cards += '<h5><a href="'+url+'" target="_blank">'+name+'</a></h5>'
        cards += ph
        cards += '<p class="text-muted">'+desc+'</p></div></div>'
    body = '<h2 class="mb-4">Resources &amp; Hotlines</h2><div class="row">'+cards+'</div>'
    return page("Resources", body)

@app.route("/pdf")
def pdf_report():
    st = request.args.get("state","")
    cr = request.args.get("crime","")
    data = DB.get((st, cr))
    if not data: return redirect("/rights")
    sn = STATES.get(st, st)
    cn = CRIMES.get(cr, cr)
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter, topMargin=0.75*inch)
        styles = getSampleStyleSheet()
        ts = ParagraphStyle("VAt", parent=styles["Title"], fontSize=18, textColor=colors.HexColor("#2C1654"))
        hs = ParagraphStyle("VAh", parent=styles["Heading2"], textColor=colors.HexColor("#6C3FA0"))
        story = [Paragraph("Victim Advocate - Rights Report", ts), Spacer(1,12)]
        story.append(Paragraph(cn+" - "+sn, hs))
        story.append(Spacer(1,12))
        td = [["Category","Details"],["Your Rights",data["rights"]],
              ["Statute of Limitations",data["sol"]],
              ["Mandatory Reporting",data["reporting"]],
              ["Compensation",data["compensation"]]]
        t = Table(td, colWidths=[1.8*inch, 4.7*inch])
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#2C1654")),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
            ("FONTSIZE",(0,0),(-1,-1),9),
            ("GRID",(0,0),(-1,-1),0.5,colors.grey),
            ("VALIGN",(0,0),(-1,-1),"TOP"),
        ]))
        story.append(t)
        story.append(Spacer(1,20))
        story.append(Paragraph("For informational purposes only. Not legal advice.", styles["Italic"]))
        story.append(Paragraph("Generated by Victim Advocate | AIIT Corporation", styles["Italic"]))
        doc.build(story)
        buf.seek(0)
        resp = make_response(buf.read())
        resp.headers["Content-Type"] = "application/pdf"
        resp.headers["Content-Disposition"] = "attachment; filename=rights_%s_%s.pdf" % (st,cr)
        return resp
    except ImportError:
        return page("PDF Error", '<div class="alert alert-danger">reportlab not installed.</div>')

@app.route("/about")
def about():
    b = '<h2 class="mb-4">About Victim Advocate</h2><div class="card p-4">'
    b += '<p class="lead">Built by AIIT Corporation to protect crime victims through technology.</p>'
    b += '<p>Every victim deserves to know their rights. This tool puts verified, state-specific '
    b += 'legal information at their fingertips, free.</p>'
    b += '<h5 class="mt-4">Disclaimer</h5>'
    b += '<p class="text-muted">General legal information, not legal advice. Consult an attorney.</p>'
    b += '<p class="mt-3"><strong>AIIT Corporation</strong> | Oklahoma | God is good, all the time.</p>'
    b += '</div>'
    return page("About", b)

@app.route("/api/rights", methods=["POST"])
def api_rights():
    st = request.json.get("state","") if request.json else ""
    cr = request.json.get("crime","") if request.json else ""
    data = DB.get((st, cr))
    if not data: return jsonify({"error":"No data found"}), 404
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5051, host="0.0.0.0")
