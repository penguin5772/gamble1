import os
import random
import time
import sys

base_money = 100
bank_money = 1000
dc_money = 0
turn = 0
turn2 = 1
ab = 0
remaining_lifetime_limit = 5000
life = 1

STAT_VARIABILITY_MODE = "CUSTOM"
CUSTOM_MIN_SCALE = 1
CUSTOM_MAX_SCALE = 1

def gamble():
    a = ["⭐", "💩", "🍉", "🍋", "♥️", "7", "🤡"]
    return random.choice(a)

def get_random_traits():
    if STAT_VARIABILITY_MODE == "EXTREME":
        min_scale, max_scale = 0.2, 2.5
    elif STAT_VARIABILITY_MODE == "SIMILAR":
        min_scale, max_scale = 0.9, 1.1
    elif STAT_VARIABILITY_MODE == "CUSTOM":
        min_scale, max_scale = CUSTOM_MIN_SCALE, CUSTOM_MAX_SCALE
    else:
        min_scale, max_scale = 0.7, 1.3

    traits = []
    for i in range(6):
        stat_scale = random.uniform(min_scale, max_scale)
        
        if i == 0:
            spurt = min(0.35, 0.18 * stat_scale)
            slump = min(0.15, 0.10 / stat_scale)
            min_s = int(3 * stat_scale) + 1
            max_s = int(4.5 * stat_scale) + 1

        elif i == 1:
            spurt = min(0.4, 0.22 * stat_scale)
            slump = min(0.18, 0.11 / stat_scale)
            min_s = int(2 * stat_scale) + 1
            max_s = int(4.5 * stat_scale) + 1

        elif i == 2:
            spurt = min(0.33, 0.19 * stat_scale)
            slump = min(0.16, 0.06 / stat_scale)
            min_s = int(3 * stat_scale) + 1
            max_s = int(4 * stat_scale) + 1

        elif i == 3:
            spurt = min(0.26, 0.17 * stat_scale)
            slump = min(0.30, 0.16 * stat_scale)
            min_s = int(3.5 * stat_scale) + 1
            max_s = int(5 * stat_scale) + 1

        elif i == 4:
            spurt = min(0.37, 0.22 * stat_scale)
            slump = 0.0
            min_s = int(2.5 * stat_scale) + 1
            max_s = int(3 * stat_scale) + 1

        else:
            spurt = min(0.235, 0.15 * stat_scale)
            slump = min(0.32, 0.19 * stat_scale)
            min_s = int(5 * stat_scale) + 1
            max_s = int(5 * stat_scale) + 1

        traits.append({
            "spurt_chance": spurt,
            "slump_chance": slump,
            "min_s": max(1, min_s),
            "max_s": max(2, max_s),
            "scale": stat_scale
        })
    return traits

def sport():
    global base_money
    team = ["레알 마드리드", "아스널", "뮌헨", "맨유", "바르셀로나"]
    team1, team2 = random.sample(team, 2)
    target1 = random.randint(0, 5)
    target2 = random.randint(0, 5)
    current1 = 0
    current2 = 0
    print(f"\n{team1} vs {team2}")
    while True:
        result = input(
            """--a,b 실패 시 -판돈x1.5, c 실패 시 -판돈x2--
a. 왼쪽 승 (x2)
b. 오른쪽 승 (x2)
c. 무승부 (x4)
결과 예측 : """
        )
        if result not in ["a", "b", "c"]:
            print("\n올바르지 않은 입력입니다.")
            continue
        break
    try:
        s_money = int(input("판돈 : "))
        if s_money > base_money:
            print("소지금 초과!")
            return
        elif s_money < 200:
            print("200$ 이상 배팅해야 합니다.")
            return
    except ValueError:
        print("올바르지 않은 입력입니다.")
        return
    print(f"\n{team1} vs {team2}")
    while current1 < target1 or current2 < target2:
        time.sleep(0.4)
        if current1 < target1:
            if random.random() < 0.1:
                current1 += 1
        if current2 < target2:
            if random.random() < 0.1:
                current2 += 1
        print(f"\r---{current1} : {current2}---", end="")
    time.sleep(1.5)
    print()
    if result == "a":
        if target1 > target2:
            base_money += s_money * 2
            print(f"예측 성공! {s_money * 2}$ 얻음!")
        else:
            base_money -= s_money
            print(f"예측 실패! {s_money}$ 탕진..")
    if result == "b":
        if target1 < target2:
            base_money += s_money * 2
            print(f"예측 성공! {s_money * 2}$ 얻음!")
        else:
            base_money -= s_money
            print(f"예측 실패! {s_money}$ 탕진..")
    if result == "c":
        if target1 == target2:
            base_money += s_money * 4
            print(f"예측 성공! {s_money * 4}$ 얻음!")
        else:
            base_money -= s_money
            print(f"예측 실패! {s_money}$ 탕진..")

def animate_slot():
    a1, a2, a3 = gamble(), gamble(), gamble()

    print("\n🎰 슬롯 돌리는 중...")

    for _ in range(20):
        print(f"\r[ {gamble()} | {gamble()} | {gamble()} ]", end="", flush=True)
        time.sleep(0.1)

    for _ in range(10):
        print(f"\r[ {a1} | {gamble()} | {gamble()} ]", end="", flush=True)
        time.sleep(0.1)

    for _ in range(10):
        print(f"\r[ {a1} | {a2} | {gamble()} ]", end="", flush=True)
        time.sleep(0.1)

    print(f"\r[ {a1} | {a2} | {a3} ]\n")
    return a1, a2, a3

def horse():
    global base_money
    horses = ["🔴🐎", "🟡🐎", "🟢🐎", "🔵🐎", "🟤🐎", "⚫🐎"]
    pos = [0] * 6
    goal_line = 100
    
    horses1 = {
        "a": horses[0],
        "b": horses[1],
        "c": horses[2],
        "d": horses[3],
        "e": horses[4],
        "f": horses[5]
    }
    
    horse_traits = get_random_traits()

    while True:
        horse_input = input("""
a. 🔴🐎[적토마] - [스퍼트형]
b. 🟡🐎[코딱지] - [기복심함]
c. 🟢🐎[초록]   - [슬로우 스타터]
d. 🔵🐎[파랑]   - [대역전형]
e. 🟤🐎[똥]     - [안정형]
f. ⚫🐎[흑인]   - [극단적]
말 선택하기 : """).strip()
        if horse_input not in horses1:
            print("올바르지 않은 입력")
            continue
        try:
            h_money = int(input("판돈 : "))
            if h_money < 100:
                print("100$ 미만은 베팅 불가")
                continue
            if h_money > base_money:
                print("소지금보다 많은 금액은 베팅할 수 없습니다.")
                continue
        except ValueError:
            print("올바르지 않은 입력")
            continue
        break

    selected_horse = horses1[horse_input]

    for i in range(6):
        print(f"{horses[i]}")
    print(" " * goal_line + "|🏁| GOAL")

    final_ranked_horses = []
    horse_rank_tag = [""] * 6
    horse_goals = [goal_line] * 6

    while len(final_ranked_horses) < 6:
        time.sleep(0.3)
        sys.stdout.write("\033[7F")
        
        finished_this_turn = []

        for i in range(6):
            if horses[i] not in final_ranked_horses:
                rand_val = random.random()
                trait = horse_traits[i]
                
                if i == 2:
                    progress = min(1.0, pos[i] / goal_line)
                    spurt_ch = trait["spurt_chance"] * (0.2 + 1.8 * progress)
                    slump_ch = trait["slump_chance"] * (1.8 - 1.5 * progress)
                    
                    if rand_val < spurt_ch:
                        move = random.randint(trait["min_s"], trait["max_s"])
                    elif rand_val < spurt_ch + slump_ch:
                        move = 0
                    else:
                        move = random.randint(1, 2)
                else:
                    if rand_val < trait["spurt_chance"]:
                        move = random.randint(trait["min_s"], trait["max_s"])
                    elif rand_val < trait["spurt_chance"] + trait["slump_chance"]:
                        move = 0
                    else:
                        move = random.randint(1, 2)
                
                pos[i] += move

                if pos[i] >= horse_goals[i]:
                    finished_this_turn.append((pos[i], i, horses[i]))

            tag_str = f" {horse_rank_tag[i]}" if horse_rank_tag[i] else ""
            sys.stdout.write(f"\r{' ' * pos[i]}{horses[i]}{tag_str}\033[K\n")

        # 재경기 목표 지점이 생긴 경우 뒤쪽에 연장 결승선(RE-GOAL) 표시
        max_goal = max(horse_goals)
        if max_goal > goal_line:
            goal_display = f"{' ' * goal_line}🏁 GOAL{' ' * (max_goal - goal_line - 7)}🏁 RE-GOAL"
        else:
            goal_display = f"{' ' * goal_line}🏁 GOAL"

        sys.stdout.write(f"\r{goal_display}\033[K\n")
        sys.stdout.flush()

        if finished_this_turn:
            finished_this_turn.sort(key=lambda x: x[0], reverse=True)
            
            groups = {}
            for dist, idx, h_name in finished_this_turn:
                groups.setdefault(dist, []).append((idx, h_name))

            for dist in sorted(groups.keys(), reverse=True):
                same_dist_horses = groups[dist]
                
                # 단독 도착
                if len(same_dist_horses) == 1:
                    idx, h_name = same_dist_horses[0]
                    if h_name not in final_ranked_horses:
                        final_ranked_horses.append(h_name)
                        current_rank = final_ranked_horses.index(h_name) + 1
                        horse_rank_tag[idx] = f"[{current_rank}등]"
                
                # 동점 도착 -> 해당 말들의 목표 지점을 15칸 뒤로 확장
                else:
                    tied_indices = [idx for idx, _ in same_dist_horses]
                    tie_rank_num = len(final_ranked_horses) + 1
                    
                    for idx in tied_indices:
                        horse_rank_tag[idx] = f"[공동{tie_rank_num}등! - 재경기]"
                        horse_goals[idx] += 15

    user_rank = final_ranked_horses.index(selected_horse) + 1

    print("\n----------------------------------------")
    print("🏁 [최종 경기 결과]")
    for r, h in enumerate(final_ranked_horses, 1):
        print(f"{r}등: {h}")
    print("----------------------------------------")
    print(f"내 말({selected_horse})의 최종 순위: {user_rank}등")

    if user_rank == 1:
        gain = h_money * 2
        base_money += gain
        print(f"1등! {gain}$ 얻음!")
    elif user_rank == 2:
        gain = h_money * 1.5
        base_money += gain
        print(f"2등! {gain}$ 얻음!")
    elif user_rank == 3:
        print("3등 예측 성공! 원금 유지!")
    elif user_rank == 4:
        base_money -= h_money
        print("4등.. 원금 잃음..")
    elif user_rank == 5:
            loss = h_money * 1.5
            base_money -= loss
            print(f"꼴등.. {loss}$ 잃음..")
    elif user_rank == 6:
        loss = h_money * 2
        base_money -= loss
        print(f"꼴등.. {loss}$ 잃음..")

    print(f"현재 잔액: {base_money}$")
    return

def animate_clown_gamble():
    print("🤡 광대가 운명을 정하는 중...")
    for i in range(10):
        emoji = "👑" if i % 2 == 0 else "🗑️"
        print(f"\r[ {emoji} ] 결과 대기중...", end="", flush=True)
        time.sleep(0.5)
    print("\r" + " " * 40 + "\r", end="", flush=True)

while True:
    current_loan_limit = min(bank_money, remaining_lifetime_limit)
    if current_loan_limit < 0:
        current_loan_limit = 0

    net_assets = base_money - dc_money

    if remaining_lifetime_limit == 0 and turn2 % 50 == 0:
        bank_money = 1000
        remaining_lifetime_limit = 5000
        turn2 = 1
    if dc_money >= 8000:
        print(f"\n🚨 대출 빚이 {dc_money}$로 8000$ 이상에 도달하여 강제 상환이 진행됩니다!")
        if base_money >= dc_money:
            base_money -= dc_money
            print(f"💸 소지금에서 {dc_money}$가 강제 차감되었습니다. (남은 소지금: {base_money}$)")
            dc_money = 0
        else:
            print("\n💀 소지금이 부족하여 대출 빚을 갚지 못했습니다. 파산했습니다!" * 3)
            input("\n(게임을 멈춥니다. Enter를 누르면 종료됩니다...)")
            break

    if base_money >= 50000:
        print("\n🎉 50000$ 달성! 승리했습니다!" * 5)

    print(f"\n현재 소지금 {base_money}$ | 대출 빚 {dc_money}$ (순자산: {net_assets}$)")
    choice = input(
        """----what do i do?---
a. 도박하기
b. 설명보기
c. 대출받기
d. 아르바이트
e. 자살☠️
>>> """
    )
    if choice == "a":
        choice = input("""
a. 슬롯머신
b. 스포츠 토토
c. 경마
""")
        if choice == "a":
            if base_money <= 0:
                print("\n⚠️ 소지금이 없습니다! 대출을 받거나 아르바이트를 하세요.")
                continue
            
            try:
                p_money = int(input("\n판돈 : "))
            except ValueError:
                print("올바르지 않은 입력")
                continue
            
            if p_money <= 9:
                print("10달러 이하 베팅 불가")
                continue
            
            if p_money > base_money:
                print("금액 부족")
                continue
            
            turn += 1
            if remaining_lifetime_limit == 0:
                turn2 += 1
    
            if dc_money > 0 and turn % 3 == 0:
                interest = int(dc_money * 0.2)
                dc_money += interest
                print(f"\n대출이자 +{interest}$ (누적 빚: {dc_money}$)")
    
            a1, a2, a3 = animate_slot()
    
            if a1 == a2 == a3:
                if a1 == "🤡":
                    animate_clown_gamble()
                    is_win = random.choice([True, False])
                    if is_win:
                        reward = p_money * 10
                        base_money += reward
                        print(f"👑 50% 당첨! {reward}$ 획득!")
                    else:
                        reward = p_money * 10
                        base_money -= reward
                        print(f"🗑️ 50% 실패.. {reward}$ 탕진!")
                else:
                    case = {
                        "7": 1000 + p_money * 20,
                        "♥️": p_money * 8,
                        "⭐": p_money * 10,
                        "🍉": p_money * 5,
                        "🍋": p_money * 5,
                        "💩": -p_money * 10,
                    }
                    reward = case[a1]
                    base_money += reward
                    if reward >= 0:
                        print(f"{reward}$ 얻음!")
                    else:
                        print(f"💩 똥 3개... {-reward}$ 잃음!")
    
            elif a1 == a2 or a2 == a3 or a1 == a3:
                matched = a1 if (a1 == a2 or a1 == a3) else a2
                if matched == "🤡":
                    animate_clown_gamble()
                    is_win = random.choice([True, False])
                    if is_win:
                        reward = p_money * 3
                        base_money += reward
                        print(f"👑 🤡 광대 성공! {reward}$ 획득!")
                    else:
                        reward = p_money * 3
                        base_money -= reward
                        print(f"🗑️ 🤡 광대 실패... {reward}$ 탕진!")
                elif matched == "💩":
                    base_money -= p_money * 2
                    print(f"💩 2개 당첨... {p_money * 2}$ 탕진!")
                elif matched == "7":
                    base_money += 500
                    print("7 2개 당첨... 500$ 얻음!")
                else:
                    base_money += int(p_money * 2)
                    print(f"{int(p_money * 2)}$ 얻음!")
            else:
                base_money -= p_money
                print(f"{p_money}$ 탕진!")
        if choice == "b":
            turn += 1
            if remaining_lifetime_limit == 0:
                turn2 += 1
            if dc_money > 0 and turn % 3 == 0:
                interest = int(dc_money * 0.2)
                dc_money += interest
                print(f"\n대출이자 +{interest}$ (누적 빚: {dc_money}$)")
            sport()
        if choice == "c":
            turn += 1
            if remaining_lifetime_limit == 0:
                turn2 += 1
            if dc_money > 0 and turn % 3 == 0:
                interest = int(dc_money * 0.2)
                dc_money += interest
                print(f"\n대출이자 +{interest}$ (누적 빚: {dc_money}$)")
            horse()
    elif choice == "b":
        print("""
 7 7 7  : 1000$ + 판돈x20
⭐⭐⭐ : +판돈x10
♥️♥️♥️ : +판돈x8
🍉🍉🍉 : +판돈x5
🍋🍋🍋 : +판돈x5
🤡🤡🤡 : 50% 확률로 [+판돈x10] 또는 [-판돈x10]
💩💩💩 : -판돈x10
 7 7   : +500$
🤡 🤡   : 50% 확률로 [+판돈x3] 또는 [-판돈x3]
💩 💩   : -판돈x2
동일 2개: +판돈x2

---경마---
1등 : 판돈x2
2등 : 판돈x1.5
3등 : 판돈 유지
4등 : -판돈
5등 : -판돈x1.5
6등 : -판돈x2

---스포츠 토토---
승리 맞출 시 판돈x2, 
무승부 맞출 시 판돈x4
실패 시 -판돈
""")

    elif choice == "c":
        print(
            f"""\n---현재 신청가능: {current_loan_limit}$ (남은 평생 대출한도: {remaining_lifetime_limit}$ / 5000$)---
현재 대출 빚: {dc_money}$
- 대출받은 원금만큼 평생 한도가 영구 차감됩니다 (상한 3000$)
- 대출 빚이 5000$ 이상이 되면 소지금에서 강제 상환되며, 부족 시 파산합니다
- 대출은 3턴마다 20% 이자가 중첩됩니다
- 10$ 이하는 대출 불가
- [취소]를 입력해 취소
- [갚기]를 입력해 대출갚기"""
        )

        dc = input("\n얼마를 대출하시겠습니까? : ")

        if dc == "취소":
            continue

        elif dc == "갚기":
            if dc_money == 0:
                print("갚을 대출금이 없습니다.")
                continue

            try:
                gg = int(input("금액 : "))
            except ValueError:
                print("올바르지 않은 금액입니다.")
                continue

            if gg > dc_money:
                print(f"실패 (대출금 {dc_money}$ 보다 많이 갚을 수 없음)")
                continue

            if gg > base_money:
                print("실패 (소지금 부족)")
                continue

            dc_money -= gg
            base_money -= gg
            print(f"{gg}$ 상환 완료! (남은 빚: {dc_money}$ | 남은 평생한도: {remaining_lifetime_limit}$)")
            continue

        try:
            dc = int(dc)
        except ValueError:
            print("올바르지 않은 입력")
            continue

        if dc > current_loan_limit:
            print(f"대출 한도 초과 (현재 신청 가능: {current_loan_limit}$)")
            continue

        if dc <= 10:
            print("소액 대출 불가")
            continue

        remaining_lifetime_limit -= dc
        dc_money += dc
        base_money += dc
        bank_money = min(1000, remaining_lifetime_limit)
        print(f"{dc}$ 대출 완료! (남은 평생 대출한도: {remaining_lifetime_limit}$)")

    elif choice == "d":
        job_type = random.choice(["type", "math"])
        ab += 1
        if dc_money > 0 and ab % 20 == 0:
            interest = int(dc_money * 0.2)
            dc_money += interest
            print(f"\n대출이자 +{interest}$ (누적 빚: {dc_money}$)")
        if job_type == "type":
            target_text = "어서오세요손님주문하신음식을맛있게준비해드릴테니잠시만기다려주시면정말감사하겠습니다"

            print("""\n---다음 문장을 띄어쓰기 없이 똑같이 입력하시오---
어서오세요 손님 주문하신 음식을 맛있게 준비해 드릴 테니 잠시만 기다려 주시면 정말 감사하겠습니다
--------------------------------------------------------------------------------""")

            txt = input("\n입력 : ")

            if txt.replace(" ", "") == target_text:
                base_money += 50
                print("50$ 입금!")
            else:
                print("오타 발생!")

        elif job_type == "math":
            print(f"\n---3문제를 모두 맞혀야 합니다 (문제당 제한시간 5초)---")
            all_correct = True

            for i in range(1, 4):
                op = random.choice(["+", "-", "*"])

                if op == "*":
                    num1 = random.randint(2, 12)
                    num2 = random.randint(2, 12)
                    correct_ans = num1 * num2
                elif op == "+":
                    num1 = random.randint(1, 50)
                    num2 = random.randint(1, 50)
                    correct_ans = num1 + num2
                else:
                    num1 = random.randint(1, 50)
                    num2 = random.randint(1, 50)
                    correct_ans = num1 - num2

                start_time = time.time()
                try:
                    user_ans_str = input(f"[{i}/3] {num1} {op} {num2} = ")
                    elapsed_time = time.time() - start_time

                    if elapsed_time > 5.0:
                        print(f"⏰ 시간 초과! ({elapsed_time:.2f}초 걸림)")
                        all_correct = False
                        break

                    user_ans = int(user_ans_str)
                    if user_ans != correct_ans:
                        print(f"오답입니다! (정답: {correct_ans})")
                        all_correct = False
                        break

                except ValueError:
                    print("숫자만 입력하시오!")
                    all_correct = False
                    break

            if all_correct:
                base_money += 50
                print("50$ 입금!")
            else:
                print("알바비 지급 실패.")

        continue

    elif choice == "e":
        life += 1
        print(f"""자살을 선택하였습니다.
현재 {life}회차""")
        base_money = 100
        bank_money = 1000
        dc_money = 0
        turn = 0
        turn2 = 1
        ab = 0
        remaining_lifetime_limit = 5000