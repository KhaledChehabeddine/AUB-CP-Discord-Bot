import codeforces_api, requests, re
from cDatabase.DB_Users import DB_Users
from helper.cTime import get_in_date_format

db_users = DB_Users('db_users')

cf_api = codeforces_api.CodeforcesApi()

class CF_API():
  def user_info(self, user):
    return cf_api.user_info([user.handle])[0]

  def user_status(self, user):
    return cf_api.user_status(user.handle)

  def user_rating(self, handle):
    lst = cf_api.user_info([handle])[0]
    return lst['rating']

  def contest_rating_changes(self, contest_id):
    try:
      lst = cf_api.contest_rating_changes(contest_id)
      arr = db_users.values()
      res = []
      contest = str()
      for user in lst:
        if len(contest) == 0: contest = user.contest_name
        if not user.handle in arr: continue
        res.append((user.rank, user.handle, user.old_rating, user.new_rating))
      res.sort()
      return res, contest
    except Exception:
      return None

  def solved_problems(self, user):
    d = {}
    solved = set()
    total = gym = 0

    for prob in self.user_status(user):
      if prob.verdict != "OK": continue

      try: id = str(prob.problem.contest_id) + prob.problem.index
      except: 
        try: id = str(prob.problem.problemset_name) + prob.problem.index
        except: continue

      if id in solved: continue
      solved.add(id)

      if prob.problem.rating == None:
        gym += 1
        continue

      total += 1
      index = prob.problem.index.strip('1234567890')
      if d.get(index): d[index] += 1
      else: d[index] = 1

    return {'total': total + gym, 'problemset': total, 'gym': gym, 'problems': sorted(d.items())}

  def solved_ratings(self, user):
    d = {}
    solved = set()

    for prob in self.user_status(user):
      if prob.verdict != "OK": continue

      try: id = str(prob.problem.contest_id) + prob.problem.index
      except: 
        try: id = str(prob.problem.problemset_name) + prob.problem.index
        except: continue

      if id in solved: continue
      solved.add(id)

      if prob.problem.rating == None: continue

      index = prob.problem.rating
      if d.get(index): d[index] += 1
      else: d[index] = 1

    return list(d.items())

  def user_rank(self, user):
    rating = self.user_rating(user.handle)
    if (rating == None): return "Inactive"
    if (rating < 1200): return "Newbie"
    if (rating < 1400): return "Pupil"
    if (rating < 1600): return "Specialist"
    if (rating < 1900): return "Expert"
    if (rating < 2200): return "Candidate Master"
    if (rating < 2300): return "Master"
    if (rating < 2400): return "International Master"
    if (rating < 2600): return "Grandmaster"
    if (rating < 2900): return "International Grandmaster"
    return "Legendary Grandmaster"