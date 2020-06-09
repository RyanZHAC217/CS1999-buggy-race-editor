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
    return render_template("buggy-form.html", buggy = None)
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
    
    total_cost = 0
    tyre_type_costs = {"knobbly":15, "slick":10, "steelband":20, "reactive":40, "maglev":50}
    power_type_costs = {"petrol":4, "fusion":400, "steam":3, "bio":5, "electric":20, "rocket":16, "hamster":3, "thermo":300, "solar":40, "wind":20}
    armour_type_costs = {"none":0, "wood":40, "aluminium":200, "thinsteel":100, "thicksteel":200, "titanium":290}
    attack_type_costs = {"none":0, "spike":5, "flame":20, "charge":28, "biohazard":30}

    if qty_wheels.isdigit() == True:
      qty_wheels = int(qty_wheels)
      if qty_tyres.isdigit() == True:
        qty_tyres = int(qty_tyres)
        if qty_attacks.isdigit() == True:
          qty_attacks = int(qty_attacks)
          if power_units.isdigit() == True:
            power_units = int(power_units)
            if aux_power_units.isdigit() == True:
              aux_power_units = int(aux_power_units)
              if hamster_booster.isdigit() == True:
                hamster_booster = int(hamster_booster)
                if qty_wheels % 2 == 0:
                  if qty_tyres >= qty_wheels:
                    tyre_cost = (qty_tyres*tyre_type_costs[tyres])
                    power_cost = (power_units*power_type_costs[power_type])
                    aux_power_cost = 0
                    if aux_power_type != 'none':
                      aux_power_cost = (aux_power_units*power_type_costs[aux_power_type])
                    attack_cost = (qty_attacks*attack_type_costs[attack])
                    armour_cost = armour_type_costs[armour]
                    if qty_wheels > 4:
                      extra_cost = qty_wheels - 4
                      armour_cost *= (1 + (extra_cost/10))
                    hamster_cost = hamster_booster*5
                    if fireproof == 'True':
                      total_cost += 70
                    if insulated == 'True':
                      total_cost += 100
                    if antibiotic == 'True':
                      total_cost += 90
                    if banging == 'True':
                      total_cost += 42
                    total_cost += tyre_cost + power_cost + aux_power_cost + attack_cost + armour_cost + hamster_cost
                    try:
                      buggy_id = request.form['id']
                      with sql.connect(DATABASE_FILE) as con:
                        cur = con.cursor()
                        if buggy_id.isdigit():
                          cur.execute('''UPDATE buggies set qty_wheels=?, flag_color=?, flag_color_secondary=?, flag_pattern=?,
                          qty_tyres=?, tyres=?, armour=?, power_type=?, power_units=?, aux_power_type=?, aux_power_units=?, hamster_booster=?,
                          attack=?, qty_attacks=?, fireproof=?, insulated=?, antibiotic=?, banging=?, algo=?, total_cost=? WHERE id=?''', 
                          (qty_wheels, flag_color, flag_color_secondary, flag_pattern, qty_tyres, tyres, armour, power_type, power_units,
                          aux_power_type, aux_power_units, hamster_booster, attack, qty_attacks, fireproof, insulated, antibiotic, banging,
                          algo, total_cost, buggy_id))
                          msg = "Buggy successfully edited"
                        else:
                          cur.execute('''INSERT INTO buggies (qty_wheels, flag_color, flag_color_secondary, flag_pattern, qty_tyres, tyres, armour,
                          power_type, power_units, aux_power_type, aux_power_units, hamster_booster, attack, qty_attacks, fireproof, insulated,
                          antibiotic, banging, algo, total_cost) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (qty_wheels, flag_color,
                          flag_color_secondary, flag_pattern, qty_tyres, tyres, armour, power_type, power_units, aux_power_type, aux_power_units,
                          hamster_booster, attack, qty_attacks, fireproof, insulated, antibiotic, banging, algo, total_cost))
                          msg = "Record successfully saved"
                        con.commit()
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
                msg = "Error, invalid input. Hamster booster must be an integer!"
                return render_template("updated.html", msg = msg)
            else:
                msg = "Error, invalid input. Auxiliary motive power units must be an integer!"
                return render_template("updated.html", msg = msg)
          else:
                msg = "Error, invalid input. Primary motive power units must be an integer!"
                return render_template("updated.html", msg = msg)
      else:
        msg = "Error, invalid input. Number of tyres must be an integer!"
      return render_template("updated.html", msg = msg)
    else:
      msg = "Error, invalid input. Number of wheels must be an integer!"
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
  records = cur.fetchall(); 
  return render_template("buggy.html", buggies = records)

#------------------------------------------------------------
# a page to edit the buggy
#------------------------------------------------------------
@app.route('/edit/<buggy_id>')
def edit_buggy(buggy_id):
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies WHERE id=?", (buggy_id))
  record = cur.fetchone(); 
  return render_template("buggy-form.html", buggy = record)

#------------------------------------------------------------
# get JSON from current record
#   this is still probably right, but we won't be
#   using it because we'll be dipping diectly into the
#   database
#------------------------------------------------------------
@app.route('/json/<buggy_id>', methods = ['POST'])
def summary(buggy_id):
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (buggy_id))
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
@app.route('/delete/<buggy_id>', methods = ['POST'])
def delete_buggy(buggy_id):
  try:
    msg = "deleting buggy"
    with sql.connect(DATABASE_FILE) as con:
      cur = con.cursor()
      cur.execute("DELETE FROM buggies WHERE id=?", (buggy_id))
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
