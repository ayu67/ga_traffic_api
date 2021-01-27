import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
connection_string =  'postgresql://postgres:letterpen@localhost:5432/ga_traffic_stops'
# connection_string = 'postgres://dkckrqblbuejjw:b51876501e6a35b8c6a9bf0555f970110a5aae9a34435d05e53f37c4be7d55c2@ec2-34-194-198-238.compute-1.amazonaws.com:5432/dm8glg0qkh59t'
engine = create_engine(connection_string)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/data<br/>"
        f"/test"
    )

@app.route("/data")
def db_to_json():
    data = []
    stops = engine.execute(f'select * from traffic_2016')
    for stop in stops:
        data.append({
            'date': stop['date'],
            'time': stop['time'],
            'lat': stop['lat'],
            'lng': stop['lng'],
            'county_name': stop['county_name'],
            'subject_race': stop['subject_race'],
            'subject_sex': stop['subject_sex'],
            'violation': stop['violation'],
            'outcome': stop['outcome'],
            'vehicle_color': stop['vehicle_color'],
            'vehicle_make': stop['vehicle_make'],
            'vehicle_model': stop['vehicle_model'],
            'vehicle_year': stop['vehicle_year'],
            'violation_count': stop['violation_count']
        })
    return jsonify(data = data)


if __name__ == '__main__':
    app.run(debug=True)
