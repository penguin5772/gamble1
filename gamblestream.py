import streamlit as st
import random
import time

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="simple gamble game", page_icon="🎰", layout="centered")

# --- 기본 변수 및 상태(Session State) 초기화 ---
if "base_money" not in st.session_state:
    st.session_state.base_money = 100
if "bank_money" not in st.session_state:
    st.session_state.bank_money = 1000
if "dc_money" not in st.session_state:
    st.session_state.dc_money = 0
if "turn" not in st.session_state:
    st.session_state.turn = 0
if "turn2" not in st.session_state:
    st.session_state.turn2 = 1
if "ab" not in st.session_state:
    st.session_state.ab = 0
if "remaining_lifetime_limit" not in st.session_state:
    st.session_state.remaining_lifetime_limit = 5000
if "life" not in st.session_state:
    st.session_state.life = 1
if "math_questions" not in st.session_state:
    st.session_state.math_questions = None
if "math_start_time" not in st.session_state:
    st.session_state.math_start_time = 0

STAT_VARIABILITY_MODE = "CUSTOM"
CUSTOM_MIN_SCALE = 1
CUSTOM_MAX_SCALE = 1

# --- 도박 로직 함수들 ---
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

def add_turn():
    st.session_state.turn += 1
    if st.session_state.remaining_lifetime_limit == 0:
        st.session_state.turn2 += 1
    if st.session_state.dc_money > 0 and st.session_state.turn % 3 == 0:
        interest = int(st.session_state.dc_money * 0.2)
        st.session_state.dc_money += interest
        st.warning(f"🚨 대출이자 발생! +{interest}$ (누적 빚: {st.session_state.dc_money}$)")

# --- 상태 확인 및 한도 처리 ---
current_loan_limit = min(st.session_state.bank_money, st.session_state.remaining_lifetime_limit)
if current_loan_limit < 0:
    current_loan_limit = 0

if st.session_state.remaining_lifetime_limit == 0 and st.session_state.turn2 % 50 == 0:
    st.session_state.bank_money = 1000
    st.session_state.remaining_lifetime_limit = 5000
    st.session_state.turn2 = 1

net_assets = st.session_state.base_money - st.session_state.dc_money

# --- 사이드바: 현재 통계 표시 ---
st.sidebar.title("📊 내 자산 및 정보")
st.sidebar.metric("소지금", f"{st.session_state.base_money}$")
st.sidebar.metric("대출 빚", f"{st.session_state.dc_money}$")
st.sidebar.metric("순자산", f"{net_assets}$")
st.sidebar.write("---")
st.sidebar.write(f"**현재 회차:** {st.session_state.life}회차")
st.sidebar.write(f"**남은 평생 대출한도:** {st.session_state.remaining_lifetime_limit}$ / 5000$")

# --- 파산 / 승리 조건 체크 ---
if st.session_state.dc_money >= 8000:
    st.error(f"🚨 대출 빚이 {st.session_state.dc_money}$로 8000$ 이상에 도달하여 강제 상환이 진행됩니다!")
    if st.session_state.base_money >= st.session_state.dc_money:
        st.session_state.base_money -= st.session_state.dc_money
        st.session_state.dc_money = 0
        st.success(f"💸 소지금에서 강제 차감되었습니다. 남은 소지금: {st.session_state.base_money}$")
    else:
        st.error("💀 소지금이 부족하여 대출 빚을 갚지 못했습니다. 파산했습니다!")
        st.stop()

if st.session_state.base_money >= 50000:
    st.balloons()
    st.success("🎉🎉🎉 50000$ 달성! 최종 승리하셨습니다! 🎉🎉🎉")

# --- 메인 화면 ---
st.title("🎰 인생역전 도박 게임")

tabs = st.tabs(["🎰 슬롯머신", "⚽ 스포츠 토토", "🐎 경마", "💡 설명보기", "🏦 대출받기", "💼 아르바이트", "☠️ 자살(리셋)"])

# 1. 슬롯머신
with tabs[0]:
    st.header("🎰 슬롯머신")
    if st.session_state.base_money <= 0:
        st.error("⚠️ 소지금이 없습니다! 대출을 받거나 아르바이트를 하세요.")
    else:
        p_money = st.number_input("판돈을 입력하세요 ($)", min_value=10, max_value=st.session_state.base_money, value=min(10, st.session_state.base_money), key="slot_bet")
        if st.button("🎰 슬롯 돌리기!", key="btn_slot"):
            add_turn()
            
            slot_placeholder = st.empty()
            for _ in range(10):
                slot_placeholder.markdown(f"### [ {gamble()} | {gamble()} | {gamble()} ]")
                time.sleep(0.08)
            
            a1, a2, a3 = gamble(), gamble(), gamble()
            slot_placeholder.markdown(f"## 🎯 결과: [ {a1} | {a2} | {a3} ]")
            
            if a1 == a2 == a3:
                if a1 == "🤡":
                    clown_placeholder = st.empty()
                    for i in range(6):
                        emoji = "👑" if i % 2 == 0 else "🗑️"
                        clown_placeholder.markdown(f"🤡 광대가 운명을 정하는 중... [ {emoji} ]")
                        time.sleep(0.3)
                    
                    if random.choice([True, False]):
                        reward = p_money * 10
                        st.session_state.base_money += reward
                        st.success(f"👑 50% 당첨! {reward}$ 획득!")
                    else:
                        reward = p_money * 10
                        st.session_state.base_money -= reward
                        st.error(f"🗑️ 50% 실패.. {reward}$ 탕진!")
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
                    st.session_state.base_money += reward
                    if reward >= 0:
                        st.balloons()
                        st.success(f"🎉 대박! {reward}$ 얻음!")
                    else:
                        st.error(f"💩 똥 3개... {-reward}$ 잃음!")
            
            elif a1 == a2 or a2 == a3 or a1 == a3:
                matched = a1 if (a1 == a2 or a1 == a3) else a2
                if matched == "🤡":
                    if random.choice([True, False]):
                        reward = p_money * 3
                        st.session_state.base_money += reward
                        st.success(f"👑 광대 성공! {reward}$ 획득!")
                    else:
                        reward = p_money * 3
                        st.session_state.base_money -= reward
                        st.error(f"🗑️ 광대 실패... {reward}$ 탕진!")
                elif matched == "💩":
                    st.session_state.base_money -= p_money * 2
                    st.error(f"💩 똥 2개... {p_money * 2}$ 탕진!")
                elif matched == "7":
                    st.session_state.base_money += 500
                    st.success("7 2개 당첨! 500$ 얻음!")
                else:
                    gain = int(p_money * 2)
                    st.session_state.base_money += gain
                    st.success(f"🎉 당첨! {gain}$ 얻음!")
            else:
                st.session_state.base_money -= p_money
                st.error(f"😭 실패... {p_money}$ 탕진!")
            st.rerun()

# 2. 스포츠 토토
with tabs[1]:
    st.header("⚽ 스포츠 토토")
    team = ["레알 마드리드", "아스널", "뮌헨", "맨유", "바르셀로나"]
    
    if "s_teams" not in st.session_state:
        st.session_state.s_teams = random.sample(team, 2)
    
    t1, t2 = st.session_state.s_teams
    st.subheader(f"🏟️ 매치: {t1} vs {t2}")
    
    s_predict = st.radio("결과 예측", ["a. 왼쪽 승 (x2)", "b. 오른쪽 승 (x2)", "c. 무승부 (x4)"])
    s_money = st.number_input("판돈 입력 (최소 200$)", min_value=200, max_value=max(200, st.session_state.base_money), value=min(200, st.session_state.base_money), key="sport_bet")
    
    if st.button("경기 진행하기", key="btn_sport"):
        if s_money > st.session_state.base_money:
            st.error("소지금이 부족합니다.")
        else:
            add_turn()
            target1, target2 = random.randint(0, 5), random.randint(0, 5)
            
            score_place = st.empty()
            c1, c2 = 0, 0
            while c1 < target1 or c2 < target2:
                time.sleep(0.15)
                if c1 < target1 and random.random() < 0.2: c1 += 1
                if c2 < target2 and random.random() < 0.2: c2 += 1
                score_place.markdown(f"### ⚽ 경기 중... {t1} **{c1} : {c2}** {t2}")
            
            score_place.markdown(f"## 🏁 최종 스코어: {t1} **{c1} : {c2}** {t2}")
            
            predict_type = s_predict[0]
            if predict_type == "a":
                if target1 > target2:
                    st.session_state.base_money += s_money * 2
                    st.success(f"🎉 예측 성공! {s_money * 2}$ 얻음!")
                else:
                    st.session_state.base_money -= s_money
                    st.error(f"😭 예측 실패! {s_money}$ 탕진..")
            elif predict_type == "b":
                if target1 < target2:
                    st.session_state.base_money += s_money * 2
                    st.success(f"🎉 예측 성공! {s_money * 2}$ 얻음!")
                else:
                    st.session_state.base_money -= s_money
                    st.error(f"😭 예측 실패! {s_money}$ 탕진..")
            elif predict_type == "c":
                if target1 == target2:
                    st.session_state.base_money += s_money * 4
                    st.success(f"🎉 예측 성공! {s_money * 4}$ 얻음!")
                else:
                    st.session_state.base_money -= s_money
                    st.error(f"😭 예측 실패! {s_money}$ 탕진..")
            
            st.session_state.s_teams = random.sample(team, 2)
            st.rerun()

# 3. 경마
with tabs[2]:
    st.header("🐎 경마 경기장")
    horses = ["🔴🐎 적토마", "🟡🐎 코딱지", "🟢🐎 초록", "🔵🐎 파랑", "🟤🐎 똥", "⚫🐎 흑인"]
    
    selected_horse_idx = st.selectbox("베팅할 말을 선택하세요:", range(6), format_func=lambda x: horses[x])
    h_money = st.number_input("판돈 입력 (최소 100$)", min_value=100, max_value=max(100, st.session_state.base_money), value=min(100, st.session_state.base_money), key="horse_bet")
    
    if st.button("경주 시작!", key="btn_horse"):
        if h_money > st.session_state.base_money:
            st.error("소지금이 부족합니다.")
        else:
            add_turn()
            horse_traits = get_random_traits()
            pos = [0] * 6
            goal_line = 40
            horse_symbols = ["🔴🐎", "🟡🐎", "🟢🐎", "🔵🐎", "🟤🐎", "⚫🐎"]
            
            race_place = st.empty()
            final_ranked = []
            
            for step in range(30):
                time.sleep(0.1)
                race_str = "```\n"
                for i in range(6):
                    if horse_symbols[i] not in final_ranked:
                        trait = horse_traits[i]
                        rand_val = random.random()
                        if rand_val < trait["spurt_chance"]:
                            pos[i] += random.randint(trait["min_s"], trait["max_s"])
                        elif rand_val < trait["spurt_chance"] + trait["slump_chance"]:
                            pos[i] += 0
                        else:
                            pos[i] += random.randint(1, 2)
                        
                        if pos[i] >= goal_line and horse_symbols[i] not in final_ranked:
                            final_ranked.append(horse_symbols[i])
                    
                    space = " " * min(pos[i], goal_line)
                    race_str += f"{space}{horse_symbols[i]}\n"
                race_str += "```"
                race_place.markdown(race_str)
                if len(final_ranked) == 6: break

            for h in horse_symbols:
                if h not in final_ranked: final_ranked.append(h)

            user_horse_symbol = horse_symbols[selected_horse_idx]
            user_rank = final_ranked.index(user_horse_symbol) + 1
            
            st.subheader("🏁 최종 경기 순위")
            for r, h in enumerate(final_ranked, 1):
                st.write(f"**{r}등**: {h}")
            
            st.info(f"선택한 말({user_horse_symbol})의 순위: **{user_rank}등**")
            
            if user_rank == 1:
                gain = h_money * 2
                st.session_state.base_money += gain
                st.success(f"1등! {gain}$ 얻음!")
            elif user_rank == 2:
                gain = int(h_money * 1.5)
                st.session_state.base_money += gain
                st.success(f"2등! {gain}$ 얻음!")
            elif user_rank == 3:
                st.info("3등! 원금 유지")
            elif user_rank == 4:
                st.session_state.base_money -= h_money
                st.error(f"4등.. {h_money}$ 잃음..")
            elif user_rank == 5:
                loss = int(h_money * 1.5)
                st.session_state.base_money -= loss
                st.error(f"5등.. {loss}$ 잃음..")
            elif user_rank == 6:
                loss = h_money * 2
                st.session_state.base_money -= loss
                st.error(f"6등.. {loss}$ 잃음..")
            st.rerun()

# 4. 설명보기
with tabs[3]:
    st.header("💡 슬롯 / 경마 / 토토 배당률 안내")
    st.markdown("""
    ### 🎰 슬롯머신
    - **7 7 7** : 1000$ + 판돈x20
    - **⭐ ⭐ ⭐** : +판돈x10
    - **♥️ ♥️ ♥️** : +판돈x8
    - **🍉 🍉 🍉 / 🍋 🍋 🍋** : +판돈x5
    - **🤡 🤡 🤡** : 50% 확률로 [+판돈x10] 또는 [-판돈x10]
    - **💩 💩 💩** : -판돈x10
    - **7 2개** : +500$
    - **🤡 2개** : 50% 확률로 [+판돈x3] 또는 [-판돈x3]
    - **💩 2개** : -판돈x2
    - **동일 2개** : +판돈x2

    ---
    ### 🐎 경마
    - **1등**: +판돈x2 | **2등**: +판돈x1.5 | **3등**: 원금 유지
    - **4등**: -판돈 | **5등**: -판돈x1.5 | **6등**: -판돈x2

    ---
    ### ⚽ 스포츠 토토
    - **승리 맞출 시**: 판돈x2
    - **무승부 맞출 시**: 판돈x4
    - **실패 시**: -판돈
    """)

# 5. 대출받기
with tabs[4]:
    st.header("🏦 대출 및 상환 시스템")
    st.write(f"- **현재 신청 가능 금액**: {current_loan_limit}$")
    st.write(f"- **현재 대출 빚**: {st.session_state.dc_money}$")
    st.write("- **규칙**: 3턴마다 20% 이자가 누적되며, 빚이 8000$ 이상이면 강제 상환 및 파산 위험이 있습니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💵 대출받기")
        loan_amt = st.number_input("대출 금액", min_value=11, max_value=max(11, current_loan_limit), value=min(100, current_loan_limit) if current_loan_limit >= 100 else 11)
        if st.button("대출 신청"):
            if loan_amt > current_loan_limit:
                st.error("대출 한도를 초과했습니다.")
            else:
                st.session_state.remaining_lifetime_limit -= loan_amt
                st.session_state.dc_money += loan_amt
                st.session_state.base_money += loan_amt
                st.session_state.bank_money = min(1000, st.session_state.remaining_lifetime_limit)
                st.success(f"{loan_amt}$ 대출 완료!")
                st.rerun()

    with col2:
        st.subheader("💸 대출 갚기")
        pay_amt = st.number_input("상환 금액", min_value=1, max_value=max(1, st.session_state.dc_money), value=min(st.session_state.dc_money, st.session_state.base_money) if st.session_state.dc_money > 0 else 1)
        if st.button("대출 상환"):
            if st.session_state.dc_money == 0:
                st.warning("갚을 대출금이 없습니다.")
            elif pay_amt > st.session_state.base_money:
                st.error("소지금이 부족합니다.")
            elif pay_amt > st.session_state.dc_money:
                st.error("대출금보다 많이 갚을 수 없습니다.")
            else:
                st.session_state.dc_money -= pay_amt
                st.session_state.base_money -= pay_amt
                st.success(f"{pay_amt}$ 상환 완료!")
                st.rerun()

# 6. 아르바이트
with tabs[5]:
    st.header("💼 아르바이트")
    st.write("알바 성공 시 **50$**를 지급합니다!")
    
    job_choice = st.radio("""알바 종류 선택
    a. 음식점 알바
    b. 노동직
    """, ["a", "b"])
    
    if job_choice == "a":
        target_text = "어서오세요손님주문하신음식을맛있게준비해드릴테니잠시만기다려주시면정말감사하겠습니다"
        st.code("어서오세요 손님 주문하신 음식을 맛있게 준비해 드릴 테니 잠시만 기다려 주시면 정말 감사하겠습니다")
        user_input = st.text_input("위 문장을 띄어쓰기 없이 입력하세요:")
        if st.button("타자 제출"):
            st.session_state.ab += 1
            if user_input.replace(" ", "") == target_text:
                st.session_state.base_money += 50
                st.success("🎉 타자 성공! 50$ 입금되었습니다.")
            else:
                st.error("❌ 오타가 발생했습니다!")
            st.rerun()
            
    elif job_choice == "🔢 수학 문제 풀기":
        st.write("3문제를 연속으로 맞춰야 합니다!")
        if st.button("문제 새로 생성하기"):
            st.session_state.math_questions = []
            for _ in range(3):
                op = random.choice(["+", "-", "*"])
                if op == "*":
                    n1, n2 = random.randint(2, 12), random.randint(2, 12)
                    ans = n1 * n2
                elif op == "+":
                    n1, n2 = random.randint(1, 50), random.randint(1, 50)
                    ans = n1 + n2
                else:
                    n1, n2 = random.randint(1, 50), random.randint(1, 50)
                    ans = n1 - n2
                st.session_state.math_questions.append((n1, op, n2, ans))
            st.session_state.math_start_time = time.time()
        
        if st.session_state.math_questions:
            q = st.session_state.math_questions
            st.write(f"1) {q[0][0]} {q[0][1]} {q[0][2]} = ?")
            a1 = st.number_input("1번 정답", value=0, key="m1")
            st.write(f"2) {q[1][0]} {q[1][1]} {q[1][2]} = ?")
            a2 = st.number_input("2번 정답", value=0, key="m2")
            st.write(f"3) {q[2][0]} {q[2][1]} {q[2][2]} = ?")
            a3 = st.number_input("3번 정답", value=0, key="m3")
            
            if st.button("수학 정답 제출"):
                st.session_state.ab += 1
                if a1 == q[0][3] and a2 == q[1][3] and a3 == q[2][3]:
                    st.session_state.base_money += 50
                    st.success("🎉 3문제 모두 맞췄습니다! 50$ 입금되었습니다.")
                else:
                    st.error("❌ 정답이 틀렸습니다.")
                st.session_state.math_questions = None
                st.rerun()

# 7. 자살 (리셋)
with tabs[6]:
    st.header("☠️ 자살 (초기화)")
    st.warning("경고: 클릭 시 모든 자산이 초기화되고 다음 회차로 진행됩니다.")
    if st.button("☠️ 정말로 초기화하시겠습니까?"):
        st.session_state.life += 1
        st.session_state.base_money = 100
        st.session_state.bank_money = 1000
        st.session_state.dc_money = 0
        st.session_state.turn = 0
        st.session_state.turn2 = 1
        st.session_state.ab = 0
        st.session_state.remaining_lifetime_limit = 5000
        st.success(f"회차가 리셋되었습니다. 현재 {st.session_state.life}회차입니다.")
        st.rerun()