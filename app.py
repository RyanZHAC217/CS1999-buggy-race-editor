from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
app = Flask(__name__)

DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"

BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"


#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
   return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
  if request.method == 'GET':
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone(); 
    return render_template("buggy-form.html", record = record)
  elif request.method == 'POST':
    msg=""
    qty_wheels = request.form['qty_wheels']
    flag_color = request.form['flag_color']
    flag_color_secondary = request.form['flag_color_secondary']
    flag_pattern = request.form['flag_pattern']
    qty_tyres = request.form['qty_tyres']
    tyres = request.form['tyres']
    armour = request.form['armour']
    power_type = request.form['power_type']
    power_units = request.form['power_units']
    aux_power_type = request.form['aux_power_type']
    aux_power_units = request.form['aux_power_units']
    hamster_booster = request.form['hamster_booster']
    attack = request.form['attack']
    qty_attacks = request.form['qty_attacks']
    fireproof = request.form['fireproof']
    insulated = request.form['insulated']
    antibiotic = request.form['antibiotic']
    banging = request.form['banging']
    algo = request.form['algo']
    if qty_wheels.isdigit() == True:
      if int(qty_wheels) % 2 == 0:
        if int(qty_tyres) >= int(qty_wheels):
          try:
            msg = "qty_wheels={qty_wheels}" 
            with sql.connect(DATABASE_FILE) as con:
               cur = con.cursor()
               cur.execute("UPDATE buggies set qty_wheels=? , flag_color=?, flag_color_secondary=?, flag_pattern=?, qty_tyres=?, tyres=?, armour=?, power_type=?, power_units=?, aux_power_type=?, aux_power_units=?, hamster_booster=?, attack=?, qty_attacks=?, fireproof=?, insulated=?, antibiotic=?, banging=?, algo=? WHERE id=?", (qty_wheels, flag_color, flag_color_secondary, flag_pattern, qty_tyres, tyres, armour, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, attack, qty_attacks, fireproof, insulated, antibiotic, banging, algo, DEFAULT_BUGGY_ID))
               con.commit()
               msg = "Record successfully saved"
          except:
            con.rollback()
            msg = "error in update operation"
          finally:
            con.close()
            return render_template("updated.html", msg = msg)
        else:
          msg = "Error, number of tyres must be greater than or equal to number of wheels!"
          return render_template("updated.html", msg = msg)
      else:
        msg = "Error, invalid input. Must be an even amount of wheels!"
        return render_template("updated.html", msg = msg)
    else:
      msg = "Error, invalid input. Must be an integer!"
      return render_template("updated.html", msg = msg)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies")
  record = cur.fetchone(); 
  return render_template("buggy.html", buggy = record)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/new')
def edit_buggy():
  return render_template("buggy-form.html")


#------------------------------------------------------------
# get JSON from current record
#   this is still probably right, but we won't be
#   using it because we'll be dipping diectly into the
#   database
#------------------------------------------------------------
@app.route('/json')
def summary():
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))
  return jsonify(
      {k: v for k, v in dict(zip(
        [column[0] for column in cur.description], cur.fetchone())).items()
        if (v != "" and v is not None)
      }
    )

#------------------------------------------------------------
# delete the buggy
#   don't want DELETE here, because we're anticipating
#   there always being a record to update (because the
#   student needs to change that!)
#------------------------------------------------------------
@app.route('/delete', methods = ['POST'])
def delete_buggy():
  try:
    msg = "deleting buggy"
    with sql.connect(DATABASE_FILE) as con:
      cur = con.cursor()
      cur.execute("DELETE FROM buggies")
      con.commit()
      msg = "Buggy deleted"
  except:
    con.rollback()
    msg = "error in delete operation"
  finally:
    con.close()
    return render_template("updated.html", msg = msg)


if __name__ == '__main__':
   app.run(debug = True, host="0.0.0.0")
