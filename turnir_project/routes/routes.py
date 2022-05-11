from flask import Blueprint, render_template, flash, request, jsonify, redirect, url_for
from sqlalchemy import desc
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


@home.route('/competition/<int:round_no>')
def competition_view(round_no):
  participants_data = ParticipantsDB.query.filter_by(activity_status=1).all()
  round_number = round_no

  # Список id активных бойцов
  active_fighters_id_data = db.session.query(ParticipantsDB.participant_id).filter_by(activity_status=1).all()
  active_fighters_id_list = [value for value, in active_fighters_id_data]
 
  # Список красных бойцов, которые уже есть в текущем раунде
  red_fighters_fights_data = db.session.query(FightsDB.red_fighter_id).filter_by(round_number=round_no).all()
  red_fighters_id_list = [value for value, in red_fighters_fights_data]
  # Список синих бойцов, которые уже есть в текущем раунде
  blue_fighters_fights_data = db.session.query(FightsDB.blue_fighter_id).filter_by(round_number=round_no).all()
  blue_fighters_id_list = [value for value, in blue_fighters_fights_data]
  # список всех бойцов, которые уже есть в текущем раунде
  fighters_id_list = red_fighters_id_list + blue_fighters_id_list
  # список бойцов, которые активны, но еще не в текущем раунде
  free_fighters_list = list(set(active_fighters_id_list) - set(fighters_id_list))
  # если количество свободных бойцов больше одного, то берем первых двух из списка и добавляем их в красного и синего
  if len(free_fighters_list)>1:
    red_fighter_id = free_fighters_list[0]
    blue_fighter_id = free_fighters_list[1]
    new_fight = FightsDB(round_number = round_number, red_fighter_id = red_fighter_id, blue_fighter_id = blue_fighter_id)
    db.session.add(new_fight)
    try:
      db.session.commit()
      
      print("создан новый бой в круге №", round_number, ". id бойцов:", red_fighter_id, " и ", blue_fighter_id)  
    except Exception as e:
      print("не получилось создать новый бой. Ошибка:  ", e)
      db.session.rollback()
  else:
    round_number = round_number + 1
  last_created_fight = FightsDB.query.order_by(desc(FightsDB.fight_id)).first()
 
  print(last_created_fight)
  print("round_number is ", round_number)
  # print(participants_data[0].participant_first_name)
  return render_template("competition.html", fight_data = last_created_fight)