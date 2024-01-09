import streamlit as st
import requests
import time
import logging
import numpy as np
import pandas as pd
# アルタイルチャート用ライブラリ追加
import altair as alt

logging.basicConfig(level=logging.DEBUG)

URL = "http://127.0.0.1:18000/"

# サイドバーにページ選択を追加
page = st.sidebar.selectbox('Choose your page',[
                            'main',
                            'Server Registration',
                            'Server List',
                            'Server Edit',
                            'Todo Create',
                            'Todo List',
                            'Graphs'
                            ])

# mainページ
if page == 'main':
    st.title('メイン画面')

    # endpointの設定
    endpoint_servers = "servers"
    endpoint_servers_search = "servers/{servername}"
    endpoint_centers = "centers"
    endpoint_areas = "areas"

    # server,center,areaのリクエスト
    response_server = requests.get(URL + endpoint_servers)
    response_center = requests.get(URL + endpoint_centers)
    response_area = requests.get(URL + endpoint_areas)

    # areaレスポンスの取得
    if response_area.status_code == 200:
        area_data = response_area.json()

        # area プルダウンの表示
        area_names = [area["areaname"] for area in area_data]
        selection_area = st.selectbox("Area", area_names)
        st.write(f"選択中のエリア：{selection_area}")

        # centernameレスポンスの取得
        if response_center.status_code == 200:
            center_data = response_center.json()

            # centername プルダウンの表示
            center_names = [center["centername"] for center in center_data]
            selection_center = st.selectbox("Center", center_names)
            st.write(f"選択中のセンター：{selection_center}")

            # servernameレスポンスの取得
            if response_server.status_code == 200:
                server_data = response_server.json()

                # servername プルダウンの表示
                server_names = [server["servername"] for server in server_data]
                selection_server = st.selectbox("Server", server_names)
                st.write(f"選択中のサーバー：{selection_server}")

                # リストに代入
                # mached_selectionがある場合はそちらを選択
                all_selections = [selection_area, selection_center, selection_server]

                if st.button("確認", key="taskcol_confirm_button"):
                    st.write("エリア:" , all_selections[0] , "　　センター:" , all_selections[1] , "　　サーバー:" , all_selections[2])

                # リストを表示
                all_selections.append(st.selectbox("作業タスク", ("作業タスク1", "作業タスク2", "作業タスク3")))
                task2_col1, task2_col2 = st.columns((2))
                # 左のカラムに"確認"ボタンを配置、押下後に実行確認
                with task2_col1:
                    if st.button("確認", key="task_col1_confirm_button"):
                        st.write("実行しますか？")
                        st.write("作業タスク:", all_selections[3])
                        st.write("エリア:" , all_selections[0])
                        st.write("センター:" , all_selections[1])
                        st.write("サーバー:" , all_selections[2])
                        if st.button("実行", key="execution_confirm_button"):
                            st.write("実行しました")
                            st.experimental_rerun()

                # 右のカラムに"リセット"ボタンを配置
                with task2_col2:
                    if st.button("リセット",key="taskcol2_reset_button"):
                        # リセットボタンを押したときのみ、選択項目をリセット
                        st.experimental_rerun()

            else:
                st.write("Error: Could not fetch the data from the API.")

        else:
            st.write("Error: Could not fetch the data from the API.")

    else:
        st.write("Error: Could not fetch the data from the API.")



# Server Registration
elif page == 'Server Registration':
    st.title('サーバー登録画面')

    # endpointの設定
    endpoint_servers = "servers"
    endpoint_centers = "centers"
    endpoint_areas = "areas"

    # area,centerのリクエスト
    response_area = requests.get(URL + endpoint_areas)
    response_center = requests.get(URL + endpoint_centers)

    with st.form(key='server-regist'):
        servername: str = st.text_input('サーバー名', max_chars=20)

        # areaレスポンスの取得
        if response_area.status_code == 200:
            area_data = response_area.json()

            # areaname プルダウンの表示
            area_names = [area["areaname"] for area in area_data]
            selection_area = st.selectbox("Area", area_names)

            # centername レスポンスの取得
            if response_center.status_code == 200:
                center_data = response_center.json()

                # centername プルダウンの表示
                center_names = [center["centername"] for center in center_data]
                selection_center = st.selectbox("Center", center_names)

                data = {
                    'servername': servername,
                    #プルダウンで表示されているareaのidを取得
                    'area_id' : area_names.index(selection_area)+1,
                    #プルダウンで表示されているcenterのidを取得
                    'center_id' : center_names.index(selection_center)+1
                }
                submit_button = st.form_submit_button(label='登録')

                if submit_button:
                    response_server = requests.post(
                        URL + endpoint_servers,
                        json=data
                        )

                    if response_server.status_code == 201:
                        st.success('Server登録完了')
                        st.write("Server名:", servername, "を登録しました。")

                    elif response_server.status_code == 400 and response_server.json().get("detail") == "Servername is empty":
                        st.error("サーバー名が空です。")

                    elif response_server.status_code == 400 and response_server.json().get("detail") == "Servername already exists":
                        st.error("同じ名前のサーバー名があります。")

                    elif response_server.status_code == 400 and response_server.json().get("detail") == "Servername contains spaces":
                        st.error("サーバー名に空白は使用できません。")

                    elif response_server.status_code == 400 and response_server.json().get("detail") == "Servername contains full-width characters":
                        st.error("サーバー名に全角文字は使用できません。")

                    else:
                        st.error("エラーが発生しました。")
                        # st.write(data)

            else:
                st.write("Error: Could not fetch the data from the Center API.")
        else:
            st.write("Error: Could not fetch the data from the Area API.")


# Server List
# Server一覧画面
elif page == 'Server List':
    st.title('サーバー一覧画面')

    # endpointの設定
    endpoint_servers = "servers"

    # serverのリクエスト
    response_server = requests.get(URL + endpoint_servers)

    if response_server.status_code == 200:

        # read_serversで全serverを取得
        server_data = response_server.json()

        # 一覧表示
        st.dataframe(server_data)


    else:
        st.error("エラーが発生しました。")


# Server Edit
# Server編集画面
elif page == 'Server Edit':
    st.title('サーバー情報編集画面')

    # endpointの設定
    endpoint_servers = "servers"
    endpoint_servers_search = "servers/id/"
    endpoint_servers_update = "servers/"
    endpoint_servers_delete = "servers/"
    endpoint_centers = "centers"
    endpoint_areas = "areas"

    # server,center,areaのリクエスト
    response_server = requests.get(URL + endpoint_servers)
    response_server_id = requests.get(URL + endpoint_servers_search)
    response_center = requests.get(URL + endpoint_centers)
    response_area = requests.get(URL + endpoint_areas)

    # serverレスポンスの取得
    if response_server.status_code == 200:
        # servername レスポンスの取得
        server_data = response_server.json()

        # servernameをプルダウン表示
        server_names = [server["servername"] for server in server_data]
        selection_server = st.selectbox("Server", server_names)

        # 選択したサーバーのidを取得
        server_ids = [server["id"] for server in server_data]
        server_id = str(server_ids[server_names.index(selection_server)])

        # with st.form(key='server-edit'):
        #     edit_button = st.form_submit_button(label='編集')

        if server_id:
            # idが一致するserverのリクエスト
            response_server = requests.get(URL + endpoint_servers_search + server_id)

            # servername,areaname,centernameのレスポンスの取得と表示
            if response_server.status_code == 200:

                # servername レスポンスの取得
                server_data = response_server.json()
                # servernameをインプットボックスに表示
                input_servername = st.text_input("Servername", server_data["servername"])

                # areaname レスポンスの取得
                area_data = response_area.json()
                # areanameをプルダウン表示
                area_names = [area["areaname"] for area in area_data]
                selection_area = st.selectbox("Area", area_names)

                # centername レスポンスの取得
                center_data = response_center.json()
                # centernameをプルダウン表示
                center_names = [center["centername"] for center in center_data]
                selection_center = st.selectbox("Center", center_names)

            elif not response_server == 200:
                st.error("エラーが発生しました。")
            else:
                pass

            # 更新ボタンと削除ボタン
            update_button = st.button(label='更新')
            delete_button = st.button(label='削除')


            if update_button:
                # 更新ボタン押下後の処理
                st.write("該当Serverの更新処理を実行します")
                data = {
                    #テキストタイプ表示されているservernameを取得
                    'servername': input_servername,
                    #プルダウンで表示されているareaのidを取得
                    'area_id' : area_names.index(selection_area)+1,
                    #プルダウンで表示されているcenterのidを取得
                    'center_id' : center_names.index(selection_center)+1,
                }
                # st.json(response_server.json())
                # st.write(data)

                # 選択したサーバーのidを取得
                response_server = requests.put(
                    URL + endpoint_servers_update + server_id,
                    json=data
                )

                if response_server.status_code == 200:
                    st.success('Server更新完了')
                    st.write("Server名:", input_servername, "の更新を完了しました。")

                elif response_server.status_code == 400 and response_server.json().get("detail") == "Servername is empty":
                    st.error("サーバー名が空です。")

                elif response_server.status_code == 400 and response_server.json().get("detail") == "Servername already exists":
                    st.error("同じ名前のサーバー名があります。")

                elif response_server.status_code == 400 and response_server.json().get("detail") == "Servername contains spaces":
                    st.error("サーバー名に空白は使用できません。")

                elif response_server.status_code == 400 and response_server.json().get("detail") == "Servername contains full-width characters":
                    st.error("サーバー名に全角文字は使用できません。")

                else:
                    st.error("エラーが発生しました。")
            else:
                pass

            # 削除ボタン押下後の処理
            if delete_button:
                st.write("該当Serverの削除処理を実行します")
                response_server = requests.delete(
                    URL + endpoint_servers_delete + server_id,
                )
                if response_server.status_code == 200:
                    st.success('Server削除完了')
                    st.write("Server名:", input_servername, "を削除しました。")

            else:
                pass


# Todo Create
# Todo登録画面
elif page == 'Todo Create':
    st.title('タスク登録画面')

    # endpointの設定
    endpoint_todos = "todos/"

    if 'todo_state' not in st.session_state:
        st.session_state.todo_state = { }

    # ユーザーが入力するタスクのタイトル
    new_todo_title = st.text_input('タイトルを入力してください', max_chars=30, )

    if new_todo_title:
        # 登録ボタンが押されたら
        if st.button('登録'):
            # 新しいタスクのデータ
            todo_data:str = {'title': new_todo_title}

            # APIにPOSTリクエストを送信して新しいタスクを登録
            response = requests.post(
                URL + endpoint_todos,
                json=todo_data
                )

            if response.status_code == 201:
                st.success('タスクが正常に登録されました。')
                time.sleep(0.5)
                st.experimental_rerun()


            else:
                st.error('エラーが発生しました。')


# Todo List
# Todo一覧画面
elif page == 'Todo List':
    st.title('タスク一覧画面')

    # endpointの設定
    endpoint_todos = "todos"

    # 初期化
    if 'todo_state' not in st.session_state:
        st.session_state.todo_state = {}

    # Todoのリクエスト
    response_todo = requests.get(URL + endpoint_todos + "/not_done")

    if response_todo.status_code == 200:
        todos = response_todo.json()

        # Streamlitのカードスタイルのデザイン
        for todo in todos:
            todo_id = todo['id']
            if todo_id not in st.session_state.todo_state:
                st.session_state.todo_state[todo_id] = todo['done']

            with st.container():
                st.write(f"**{todo['title']}**")

                # ユーザーがチェックボックスの状態を変更したときのアクション
                def on_checkbox_change():
                    complete_res = requests.put(URL + endpoint_todos + "/" + str(todo_id) + "/complete")

                    if complete_res.status_code == 200:
                        success_message = st.success("タスクが完了しました。")
                        time.sleep(0.25)  # 0.25秒間待機
                        success_message.empty()  # メッセージを削除
                        st.session_state.todo_state[todo_id] = False  # チェックボックスをリセット
                        st.experimental_rerun()
                    else:
                        st.error("タスクの更新中にエラーが発生しました。")

                # チェックボックス
                is_checked = st.checkbox("完了", value=st.session_state.todo_state[todo_id], key=str(todo_id))
                if is_checked:
                    on_checkbox_change()
                st.write("------")
    else:
        if response_todo.json().get("detail") == "Todo not found":
            st.write("タスクはありません。")

elif page == 'Graphs':
    st.title('Graphs')


    # ランダムな表データ作成（ダミー）
    data = np.random.rand(50,2)

    # データフレーム作成
    df = pd.DataFrame(data, columns=["サンプル1","サンプル2"])

    # H1見出し
    st.markdown("# グラフアプリ")

    # H3見出し
    st.markdown("### 折れ線グラフ")
    # グラフをアプリ上に表示
    st.line_chart(data=df,                     # データソース
                x="サンプル1",               # X軸
                y="サンプル2",               # Y軸
                width=0,                     # 表示設定（幅）
                height=0,                    # 表示設定（高さ）
                use_container_width=True,    # True の場合、グラフの幅を列の幅に設定
                )

    # H3見出し
    st.markdown("### 面グラフ")
    # グラフをアプリ上に表示
    st.area_chart(data=df,                     # データソース
                x="サンプル1",               # X軸
                y="サンプル2",               # Y軸
                width=0,                     # 表示設定（幅）
                height=0,                    # 表示設定（高さ）
                use_container_width=True,    # True の場合、グラフの幅を列の幅に設定
                )

    # H3見出し
    st.markdown("### 棒グラフ")

    # グラフをアプリ上に表示
    st.bar_chart(data=df,                      # データソース
                x="サンプル1",               # X軸
                y="サンプル2",               # Y軸
                width=0,                     # 表示設定（幅）
                height=0,                    # 表示設定（高さ）
                use_container_width=True,    # True の場合、グラフの幅を列の幅に設定
                )

    ## アルタイルチャート
    # H3見出し
    st.markdown("### アルタイルチャート")
    # ランダムな表データ作成（ダミー）
    data_altair = np.random.rand(50,3)
    # データフレーム作成
    df_altair = pd.DataFrame(data_altair, columns=["サンプル1","サンプル2","サンプル3"])
    # アルタイルチャート設定
    graph = alt.Chart(df_altair).mark_circle().encode(
        x     = 'サンプル1',   # X軸
        y     = 'サンプル2',   # Y軸
        size  = 'サンプル3',   # 凡例サイズ
        color = 'サンプル3',   # 凡例
        ).interactive()

    # グラフ可視化
    st.altair_chart(graph, use_container_width=False, theme="streamlit")

## login
# ログイン画面
elif page == 'login':
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.title("ログイン済み")
        st.write("ログイン済みです")
        st.write("Token:"+ st.session_state.access_token)

    else:
        st.title("ログイン画面")
        login_username:str = st.text_input("ユーザー名", max_chars=20)
        login_password:str = st.text_input("パスワード", max_chars=20, type="password")
        data = {
            "login_username": login_username,
            "login_password": login_password
        }

        if st.button("ログイン"):
            res = requests.post(
                "http://localhost:8000/login",
                json=data
            )

            if res.status_code == 200:
                st.success("ログイン成功")
                # ログイン成功時にst.session_state.logged_inをTrueにする
                st.session_state.logged_in = True
                # ログイン成功時に返ってくるトークンを取得
                response_data = res.json()
                # トークンをst.session_stateに保存
                st.session_state.access_token = response_data['access_token']
                st.session_state.refresh_token = response_data['refresh_token']
                st.session_state.token_type = response_data['token_type']

                # main画面に遷移
                st.experimental_rerun()

            else:
                st.error("ログイン失敗 ユーザー名、パスワードが間違っています。")

