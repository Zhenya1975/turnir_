from flask import Blueprint, render_template, flash, request, jsonify, redirect, url_for
from ..models.models import ParticipantsDB, FightsDB
from ..extensions import db
import csv

home = Blueprint('home', __name__, template_folder='templates')


@home.route('/')
def home_view():
    return render_template("home.html")

@home.route('/fill_fighters')
def fill_fighters():
  with open('fighters.csv', encoding='utf8') as csvfile:
    fighters_csv_list = csv.reader(csvfile)
    for row in fighters_csv_list:
      new_fighter = ParticipantsDB(participant_first_name=row[0], participant_last_name=row[1], activity_status = 1)
      db.session.add(new_fighter)
      try:
          db.session.commit()
          print("Бойцы импортированы в базу")
      except Exception as e:
          print("Не получилось импортировать бойцов. Ошибка: ", e)
          db.session.rollback()
  return "результат импорта - в принт"

def create_fight(round_no):
  round_number = round_no

  # Список id активных бойцов
  active_fighters_id_data = db.session.query(ParticipantsDB.participant_id).filter_by(activity_status=1).all()
  active_fighters_id_list = [value for value, in active_fighters_id_data]
  print("active_fighters_ids: ", active_fighters_id_list)
  # Список бойцов, которые уже есть в текущем раунде




@home.route('/competition/<int:round_no>')
def competition_view(round_no):
  participants_data = ParticipantsDB.query.filter_by(activity_status=1).all()
  current_round_no = round_no
  create_fight(current_round_no)
  
  # print(participants_data[0].participant_first_name)
  return render_template("competition.html", round_no = round_no)