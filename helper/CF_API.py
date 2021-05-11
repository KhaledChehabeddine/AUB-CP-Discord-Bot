import codeforces_api, requests, re
from cDatabase.DB_Users import DB_Users
from helper.cTime import get_in_date_format

database_users = DB_Users('db_users')
cf_api = codeforces_api.CodeforcesApi()

# ------------------------------------ { CF_API } ------------------------------------ # 
class CF_API():
    # ------------------ [ user_info() ] ------------------ # 
        # Returns information of the user
    def user_info(self, user): return cf_api.user_info([user.handle])[0]

    # ------------------ [ user_status() ] ------------------ # 
        # Returns the status of the user
    def user_status(self, user): return cf_api.user_status(user.handle)

    # ------------------ [ user_rating() ] ------------------ # 
        # Returns the current CodeForces rating of the user
    def user_rating(self, handle):
        lst = cf_api.user_info([handle])[0]
        return lst.rating

    # ------------------ [ contest_rating_changes() ] ------------------ # 
        # Returns the user's "rank", "handle", "old_rating", "new_rating" from "contest"
    def contest_rating_changes(self, contest_id):
        try:
            lst = cf_api.contest_rating_changes(contest_id)
            arr = database_users.values()
            result = []
            contest = str()
            for user in lst:
                if len(contest) == 0: contest = user.contest_name
                if not user.handle in arr: continue
                result.append((user.rank, user.handle, user.old_rating, user.new_rating))
                result.sort()
            return result, contest
        except Exception: return None

    # ------------------ [ solved_problems() ] ------------------ # 
        # Checks if the problem's verdict was "OK" before counting it
        # Returns problems solved from "problemset", "gym", and "total" = "problemset" + "gym"
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

    # ------------------ [ solved_ratings() ] ------------------ # 
        # Checks if the problem's verdict was "OK" before counting it
        # Returns the number of problems solved by the user at each difficulty rating
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

    # ------------------ [ user_rank() ] ------------------ # 
        # Returns the user's CodeForces rating, if not available then Inactive
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