import os
import re

from flask import Flask, request, render_template

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query/", methods=["GET", "POST"])
def perform_query(cmd1: str = None, value1: str = None, cmd2: str = None, value2: str = None, file_name: str = None):

    try:
        if request.method == "GET":
            try:
                file_name: str = os.path.join(DATA_DIR, request.args.get('file_name'))
            except TypeError:
                return f'Не передан аргумент "file_name"', 400
            cmd1 = request.args.get("cmd1")
            cmd2 = request.args.get("cmd2")
            value1 = request.args.get("value1")
            value2 = request.args.get("value2")
        elif request.method == "POST":
            data = request.json
            print(data)
            file_name = os.path.join(DATA_DIR, data['file_name'])
            cmd1 = data["cmd1"]
            cmd2 = data["cmd2"]
            value1 = data["value1"]
            value2 = data["value2"]

        with open(file_name, 'r', encoding='UTF-8') as f:

            result = []

            if cmd1 == 'filter':
                result = [i.strip() for i in f if value1 in i]

            elif cmd1 == 'map':
                result = [i.strip().split()[int(value1)] for i in f]

            elif cmd1 == 'unique':
                all_data = [i.strip().split()[0] for i in f]
                for i in all_data:
                    if i not in result:
                        result.append(i)

            elif cmd1 == 'sort' and value1 == 'asc':
                result = sorted([i.strip() for i in f])

            elif cmd1 == 'sort' and value1 == 'desc':
                result = sorted([i.strip() for i in f], reverse=True)

            elif cmd1 == 'limit':
                n = 1
                for i in f:
                    if n <= int(value1):
                        n += 1
                        result.append(i.strip())
            elif cmd1 == 'regex':
                result = [item for item in f if re.compile(value1).search(item)]

            if cmd2 == 'filter':
                result = [i.strip() for i in result if value2 in i]

            elif cmd2 == 'map':
                result = [i.strip().split()[int(value2)] for i in result]

            elif cmd2 == 'unique':
                all_data = [i.strip().split()[0] for i in result]
                for i in all_data:
                    if i not in result:
                        result.append(i)

            elif cmd2 == 'sort' and value2 == 'asc':
                result = sorted([i.strip() for i in result])

            elif cmd2 == 'sort' and value2 == 'desc':
                result = sorted([i.strip() for i in result], reverse=True)

            elif cmd2 == 'limit':
                n = 1
                for i in result:
                    if n <= int(value2):
                        n += 1
                        result.append(i.strip())

            elif cmd2 == 'regex':
                result = [item for item in f if re.compile(value2).search(item)]

            return render_template("response.html", data=result)
    except FileNotFoundError:
        return f'Заданный файл {file_name} не найден', 400


if __name__ == '__main__':
    app.run()
