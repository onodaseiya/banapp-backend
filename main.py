from datetime import datetime, timedelta
from typing import List

from fastapi import FastAPI, HTTPException, Path
from DBHelper import execute_query
from repositories.Achievement import Achievement
from repositories.History import History, HistoryCreate
from repositories.Pet import PetCreate, HungerUpdate
from repositories.User import UserCreate, CoinUpdate

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# -------------------- User --------------------
# テーブル全件取得
@app.get("/{table_name}/")
def read_table_all(table_name: str):
    valid_table = ["users", "pets", "achievements", "items", "histories"]
    if table_name not in valid_table:
        raise HTTPException(status_code=404, detail="Table not found")
    return execute_query(f"SELECT * FROM banapp.{table_name}")


# users挿入
@app.post("/users/")
def create_users(user: UserCreate, response_model=int):
    query = "INSERT INTO banapp.users (name, coin, cigarette_price, cigarette_per_day) VALUES (%s, 30, %s, %s)"
    values = (user.name, user.cigarette_price, user.cigarette_per_day)
    return execute_query(query, values, fetch=False, return_id=True)


@app.get("/users/{user_id}")
def read_user(user_id: int):
    query = "SELECT * FROM banapp.users WHERE id=%s"
    values = (user_id,)
    return execute_query(query, values, fetch=True)


# ユーザのコイン変更
@app.patch("/users/{user_id}/coin", response_model=dict)
def update_user_coin(coin_data: CoinUpdate, user_id: int = Path(..., description="The ID of the user to update")):
    query = "UPDATE banapp.users SET coin = %s WHERE id = %s"
    values = (coin_data.coin, user_id)
    result = execute_query(query, values, fetch=False)
    if result.get("message"):
        return {"message": f"User with id {user_id} coin updated successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")


@app.get("/users/{user_id}/histories", response_model=List[History])
def get_user_histories(user_id: int):
    # SQLクエリを作成
    query = "SELECT * FROM banapp.histories WHERE user_id=%s"
    values = (user_id,)

    # クエリ実行
    results = execute_query(query, values, fetch=True)

    if not results:
        raise HTTPException(status_code=404, detail=f"No histories found for user with id {user_id}")

    return results


@app.get("/users_coin/{user_id}/{item_id}/")
def change_coin(user_id: int, item_id: int):
    query = "SELECT * FROM banapp.items WHERE id = %s"
    values = (item_id,)
    result = execute_query(query, values, fetch=True)

    users_query = "SELECT * FROM banapp.users WHERE id = %s"
    users_values = (user_id,)
    users_result = execute_query(users_query, users_values, fetch=True)

    for row in users_result:
        coin = row.get('coin')

        for row in result:
            id = row.get('id')

            if id is not None and id == 1:
                if coin is not None and coin >= 30:
                    update_query = "UPDATE banapp.users SET coin = coin - 30 WHERE id=%s"
                    update_values = (user_id,)
                    execute_query(update_query, update_values, fetch=False)
                else:
                    return {"message": "Not enough coin"}

            elif id is not None and id == 2:
                if coin is not None and coin >= 40:
                    update_query = "UPDATE banapp.users SET coin = coin - 40 WHERE id=%s"
                    update_values = (user_id,)
                    execute_query(update_query, update_values, fetch=False)
                else:
                    return {"message": "Not enough coin"}
                

            elif id is not None and id == 3:  
                if coin is not None and coin >= 60:
                    update_query = "UPDATE banapp.users SET coin = coin - 60 WHERE id=%s"
                    update_values = (user_id,)
                    execute_query(update_query, update_values, fetch=False)
                else:
                    return {"message": "Not enough coin"}

            elif coin is not None and id == 4:
                if id is not None and coin >= 80:
                    update_query = "UPDATE banapp.users SET coin =  coin - 80 WHERE id=%s"
                    update_values = (user_id,)
                    execute_query(update_query, update_values, fetch=False)
                else:
                    return {"message": "Not enough coin"}

            elif coin is not None and id == 5:
                if id is not None and coin >= 30:
                    update_query = "UPDATE banapp.users SET coin = coin - 100 WHERE id=%s"
                    update_values = (user_id,)
                    execute_query(update_query, update_values, fetch=False)
                else:
                    return {"message": "Not enough coin"}

            else: pass

        return {"message": "successful buy"}
    
#continuedayを持ってくる
@app.get("/users/baitlogs/{user_id}")
def get_continueday(user_id: int):
    query = "SELECT * FROM banapp.baitlogs WHERE user_id = %s"
    values = (user_id,)
    return execute_query(query, values, fetch=True)

# -------------------- Pet --------------------
@app.post("/pets/", response_model=dict)
def create_pet(pet_data: PetCreate):
    query = "INSERT INTO banapp.pets (user_id, name, hunger) VALUES (%s, %s, %s)"
    values = (pet_data.user_id, pet_data.name, pet_data.hunger)
    return execute_query(query, values, fetch=False, return_id=True)


# 自分のペットのデータ
@app.get("/pets/{pet_id}")
def read_user(pet_id: int):
    query = "SELECT * FROM banapp.pets WHERE id=%s"
    values = (pet_id,)
    return execute_query(query, values, fetch=True)

@app.get("/pets/{pet_id}/death", response_model=dict)
def register_pet_death(pet_id: int):
    # 現在の時刻を取得
    death_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # SQLクエリを作成
    query = "UPDATE banapp.pets SET death_at = %s WHERE id=%s"
    values = (death_time, pet_id)

    # クエリを実行
    result = execute_query(query, values, fetch=False)

    # 結果の確認
    if result.get("message"):
        return {"death_time": death_time}
    else:
        raise HTTPException(status_code=404, detail=f"Pet with id {pet_id} not found")


# 空腹度変更
@app.patch("/pets/{pet_id}/hunger", response_model=dict)
def update_pet_hunger(hunger_data: HungerUpdate, pet_id: int = Path(..., description="The ID of the pet to update")):
    query = "UPDATE banapp.pets SET hunger = %s WHERE id=%s"
    values = (hunger_data.hunger, pet_id)
    result = execute_query(query, values, fetch=False)
    if result.get("message"):
        return {"message": f"Pet with id {pet_id} hunger updated successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Pet with id {pet_id} not found")


# -------------------- History --------------------

@app.post("/histories/")
def create_history(history: HistoryCreate):
    query = "INSERT INTO banapp.histories (user_id, pet_id, more_money) VALUES (%s, %s, %s)"
    values = (history.user_id, history.pet_id, history.more_money)
    return execute_query(query, values, fetch=False)

# -------------------- Achievement --------------------
@app.post("/achievements/")
def create_achievement(achievement: Achievement):
    query = "INSERT INTO banapp.get_achievements (user_id, achievement_id) VALUES (%s, %s)"
    values = (achievement.user_id, achievement.achievement_id)
    return execute_query(query, values, fetch=False)

@app.get("/achievements/{user_id}/")
def check_achievement(user_id: int):
    query = "SELECT achievement_id FROM banapp.get_achievements WHERE user_id=%s"
    values = (user_id,)
    return execute_query(query, values, fetch=True)

#アチーブメント達成判定
@app.get("/users/{user_id}/decision/")
def decision_achievement(user_id: int,):
    baitlog_query = "SELECT user_id, continueday, totalcount FROM banapp.baitlogs WHERE user_id = %s"
    values = (user_id,)
    result =  execute_query(baitlog_query,values, fetch=True)

    for row in result:
        continueday = row.get('continueday')
        totalcount = row.get('totalcount')

        query = ""

        if continueday is not None and continueday > 5:
            pass

        elif continueday is not None and continueday >= 5:
                #get_achievementにuser_id,achievement_idを送信
            query = "INSERT IGNORE INTO banapp.get_achievements (user_id, achievement_id) VALUES (%s, %s)"
            values = (row['user_id'], 4)
            

        elif continueday is not None and continueday >= 3:
                #get_achievementにuser_id,
            query = "INSERT IGNORE INTO banapp.get_achievements (user_id, achievement_id) VALUES (%s, %s)"
            values = (row['user_id'], 3)
            
                
        elif continueday is not None and continueday >= 1:
                #get_achievementにuser_id,achievement_idを送信
            query = "INSERT IGNORE INTO banapp.get_achievements (user_id, achievement_id) VALUES (%s, %s)"
            values = (row['user_id'], 2)
        
        else: pass
            
        execute_query(query, values, fetch=False)
            
        if totalcount is not None and totalcount > 1:
            pass

        elif totalcount is not None and totalcount >= 1:
                #get_achievementにuser_id,achievement_idを送信
            query = "INSERT IGNORE INTO banapp.get_achievements (user_id, achievement_id) VALUES (%s, %s)"
            values = (row['user_id'], 1)
            execute_query(query, values, fetch=False)

        else: pass

        return {"message": "successfully"}
            
# -------------------- Item --------------------



# -------------------- baitlog --------------------
@app.get("/users/{user_id}/baitlogs/")
def update_continueday(user_id: int):
    today = datetime.now().date()

    totalcount_query = "UPDATE banapp.baitlogs SET totalcount = totalcount + 1, log_date = CURRENT_TIMESTAMP WHERE user_id=%s"
    totalcount_values = (user_id,)
    execute_query(totalcount_query, totalcount_values, fetch=False)

    # 直近のログを取得
    latest_log_query = "SELECT * FROM banapp.baitlogs WHERE user_id = %s"
    latest_log_values = (user_id,)
    latest_log_result = execute_query(latest_log_query, latest_log_values, fetch=True)

    if latest_log_result:
        # 直近のログが存在する場合
        latest_log_date = latest_log_result[0]['log_date'].date()

        if latest_log_date == today:
            return {"message": "successfully"}

        elif latest_log_date == today - timedelta(days=1):
            # 直近のログが昨日の場合は continueday をインクリメント
            query = "UPDATE banapp.baitlogs SET continueday = continueday + 1, log_date = CURRENT_TIMESTAMP WHERE user_id=%s"
            values = (user_id)

        else:
            # 直近のログが昨日以前の場合は continueday をリセット
            query = "UPDATE banapp.baitlogs SET continueday = 1, log_date = CURRENT_TIMESTAMP WHERE user_id=%s"
            values = (user_id)

    else:
        # 直近のログが存在しない場合は continueday を初期化
        query = "UPDATE banapp.baitlogs SET continueday = 1, log_date = CURRENT_TIMESTAMP WHERE user_id=%s"
        values = (user_id)
        
    execute_query(query, values, fetch=False)
    return {"message": "success update"}
