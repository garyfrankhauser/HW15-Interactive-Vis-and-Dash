import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
from flask_sqlalchemy import SQLAlchemy

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///db/belly_button_biodiversity.sqlite")
conn = engine.connect()
Base = automap_base()
Base.prepare(engine, reflect=True)
print(Base.classes.keys())

Otu = Base.classes.otu
Samples = Base.classes.samples
Samples_meta = Base.classes.samples_metadata

inspector = inspect(engine)
inspector.get_table_names()

session = Session(engine)


#create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/names")
def names():
    sample_names=[]
    columns = inspector.get_columns('samples')
    for column in columns:
        if column['name'] != 'otu_id':
            sample_names.append(column['name'])
    return jsonify(sample_names)

@app.route("/otu")
def otu():
    results = session.query(Otu.lowest_taxonomic_unit_found).all()
    otu_desc=[result[0] for result in results]
    return jsonify(otu_desc)

@app.route('/metadata/<sample>')
def metadata(sample):
    meta_dict={}
    results = session.query(
        Samples_meta.AGE,
        Samples_meta.BBTYPE,
        Samples_meta.ETHNICITY,
        Samples_meta.GENDER,
        Samples_meta.LOCATION,
        Samples_meta.SAMPLEID
    ).filter(Samples_meta.SAMPLEID==sample[3:])

    for result in results:
        meta_dict["AGE"] = result.AGE
        meta_dict["BBTYPE"] = result.BBTYPE
        meta_dict["ETHNICITY"] = result.ETHNICITY
        meta_dict["GENDER"] = result.GENDER
        meta_dict["LOCATION"] = result.LOCATION
        meta_dict["SAMPLEID"] = result.SAMPLEID

    return jsonify(meta_dict)

@app.route('/wfreq/<sample>')
def wfreq(sample):
    wfreq_int = []
    results = session.query(
        Samples_meta.WFREQ
    ).filter(Samples_meta.SAMPLEID==sample[3:]).limit(1)

    for result in results:
        wfreq_int.append(result.WFREQ)

    return jsonify(wfreq_int)

@app.route('/samples/<sample>')
def samples(sample):
    if sample != '':
        sample_values = []
        otu_ids=[]
        results = conn.execute('SELECT otu_id, '+str(sample)+' as sample_value FROM samples where '+str(sample)+' > 0 order by '+str(sample)+' desc')

        for result in results:
            sample_values.append(result.sample_value)
            otu_ids.append(result.otu_id)
        
        output={"otu_ids":otu_ids,"sample_values":sample_values}
        return jsonify(output)

if __name__ == "__main__":
    app.run()
