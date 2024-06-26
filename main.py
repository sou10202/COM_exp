from flask import *
import random, time, math
import os

def makequestion(index, level, uplevel):
    ans = [0]*3
    if (index < uplevel):
        start = 10 ** level
        end = 10 ** (level + 1)
    else:
        start = 10 ** (level + 1)
        end = 10 ** (level + 2)
    flag = random.random()
    if (flag <= 0.5):
        ans[0] = 0
        while True:
            ans[1] = random.randint(start, end)
            if ((ans[1] % 2 == 0) or (ans[1] % 3 == 0) or (ans[1] % 5 == 0) or (ans[1] % 7 == 0) or (ans[1] % 11 == 0)):
                continue
            if ((level >= 5) and ((ans[1] % 13 == 0) or (ans[1] % 17 == 0) or (ans[1] % 19 == 0) or (ans[1] % 23 == 0))):
                continue
            else:
                sqrt_i = int(math.sqrt(ans[1]))
                for i in range(7, sqrt_i):
                    if ans[1] % i == 0:
                        ans[2] = i
                        return (ans)
                continue
    else:
        ans[0] = 1
        while True:
            mid = random.randint(start, end)
            for i in range(mid, end):
                sqrt_i = int(math.sqrt(i))
                div_if = 1
                for j in range(2, sqrt_i + 1):
                    if (i % j == 0):
                        div_if *= 0
                if (div_if == 1):
                    ans[1] = i
                    return (ans)

def makelist(level, req_num):
  ans = [0] * req_num
  uplevel = req_num // 2
  for i in range(len(ans)):
    ans[i] = makequestion(i, level, uplevel)
  return (ans)
            
def check_level(level_ja):
    if (level_ja == "初級"):
        return (2)
    elif (level_ja == "中級"):
        return (3)
    elif (level_ja == "上級"):
        return (5)
    else:
        return (7)

def chcek_rank(x):
    if (x <= 20):
        return (0)
    elif ((x > 20) and (x <=40)):
        return (20)
    elif ((x > 40) and (x <=60)):
        return (40)
    elif ((x > 60) and (x <=80)):
        return (60)
    elif ((x > 80) and (x < 100)):
        return (80)
    else:
        return (100)

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    session["c_index"] = -1
    session["rate"] = 0
    return (render_template("index.html"))

@app.route("/check", methods=["POST"])
def check():
        req_num = int(request.form.get("req_num"))
        level_ja = request.form.get("level")
        level = check_level(level_ja)
        session["questions"] = makelist(level, req_num)
        return (render_template("check.html", level=level_ja, req_num=req_num))


@app.route("/question", methods=["POST"])
def question():
    questions = session.get("questions")
    c_index = session.get("c_index") + 1
    session["c_index"] = c_index
    q_num = questions[c_index][1]
    return (render_template("question.html", index_num = c_index + 1, 
                            q_num = q_num))

@app.route("/answer", methods=["POST"])
def check_ans():
    questions = session.get("questions")
    c_index = session.get("c_index")
    rate = session.get("rate")
    user_ans = request.form.get("user_ans")
    if (((user_ans == "素数") and (questions[c_index][0] == 1))
       |((user_ans == "合成数") and (questions[c_index][0] == 0))):
        correct = 1
        session["rate"] = rate + 1
    else:
        correct = 0
    if (c_index < len(questions) - 1):
        is_final = 0
    else:
        is_final = 1
    return (render_template("answer.html", correct=correct, q_num=questions[c_index][1], 
                            divnum=questions[c_index][2], prime=questions[c_index][0], is_final=is_final))


@app.route("/final", methods=["POST"])
def final():
    rate = session.get("rate")
    questions = session.get("questions")
    final_rate = int((rate / len(questions)) * 100)
    req_num = len(questions)
    rank = chcek_rank(final_rate)
    return (render_template("final.html", rate=rate, final_rate=final_rate, req_num=req_num, rank=rank))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
      

