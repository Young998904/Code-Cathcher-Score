from flask import Flask, request, jsonify
import subprocess
import os
import uuid
import shutil

app = Flask(__name__)

@app.route('/execute/python', methods=['POST'])
def execute_python_code():
    data = request.json
    code = data['code']
    input = data['input']
    expected_output = data['output']

    # 임시 파일 경로 생성
    temp_file_path = f"./temp_{uuid.uuid4()}.py"

    # 코드를 임시 파일로 저장
    with open(temp_file_path, 'w') as file:
        file.write(code)

    try:
        # 입력값을 문자열로 전달하고, text=True 옵션을 사용하여 표준 입출력을 문자열로 처리
        process = subprocess.run(['python3', temp_file_path], input=input, text=True, capture_output=True, check=True)
        output = process.stdout.strip()

        # 출력 비교
        result = {
            "error": False,
            "error_message": None,
            "input": input,
            "expected_output": expected_output,
            "actual_output": output,
            "correct": output == expected_output
        }
    # 실행 에러 처리
    except subprocess.CalledProcessError as e:
        # 실행 에러 메시지에서 "line" 이후의 내용만 추출
        if e.stderr:
            start = e.stderr.find('line')
            error_message = e.stderr[start:] if start != -1 else "Unknown error"
        else:
            error_message = "Unknown error"
        result = {
            "error": True,
            "error_message": error_message,
            "input": input,
            "expected_output": expected_output,
            "actual_output": None,
            "correct": False
        }
    finally:
        # 임시 파일 삭제
        os.remove(temp_file_path)

    return jsonify(result)

@app.route('/execute/java', methods=['POST'])
def execute_java_code():
    data = request.json
    code = data['code']
    input = data['input']
    expected_output = data['output']

    dir_path = f"./temp/{uuid.uuid4()}"
    os.makedirs(dir_path, exist_ok=True)

    java_file_path = os.path.join(dir_path, "Main.java")
    with open(java_file_path, 'w') as java_file:
        java_file.write(code)

    try:
        # Java 코드 컴파일
        compile_process = subprocess.run(['javac', java_file_path], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        # 컴파일 오류 처리, 여러 오류에 대해 파일 경로 이후의 내용 추출
        errors = e.stderr.split('\n')
        filtered_errors = [error[error.find('/Main.java'):] if '/Main.java' in error else error for error in errors]
        error_message = "\n".join(filter(None, filtered_errors))
        result = {
            "error": True,
            "error_message": error_message,
            "input": input,
            "expected_output": expected_output,
            "actual_output": None,
            "correct": False,
        }
        shutil.rmtree(dir_path)  # 오류 발생 시 디렉터리 정리
        return jsonify(result)

    try:
        # Java 코드 실행
        execute_process = subprocess.run(['java', '-cp', dir_path, 'Main'], input=input, text=True, capture_output=True, check=True)
        output = execute_process.stdout.strip()

        result = {
            "error": False,
            "error_message": None,
            "input": input,
            "expected_output": expected_output,
            "actual_output": output,
            "correct": output == expected_output
        }
    except subprocess.CalledProcessError as e:
        # 실행 오류 처리, 여러 오류에 대해 파일 경로 이후의 내용 추출
        errors = (e.stderr if e.stderr else e.stdout).split('\n')
        filtered_errors = [error[error.find('/Main.java'):] if '/Main.java' in error else error for error in errors]
        error_message = "\n".join(filter(None, filtered_errors))
        result = {
            "error": True,
            "error_message": error_message,
            "input": input,
            "expected_output": expected_output,
            "actual_output": None,
            "correct": False,
        }
    finally:
        shutil.rmtree(dir_path)  # 작업 완료 후 디렉터리 정리

    return jsonify(result)
@app.route('/execute/js', methods=['POST'])
def execute_javascript_code():
    data = request.json
    code = data['code']  # JavaScript 코드
    input_data = data['input']  # 입력 데이터
    expected_output = data['output']  # 예상 출력 결과

    # 임시 파일 경로 생성
    temp_file_path = f"./temp_{uuid.uuid4()}.js"

    # 코드를 임시 파일로 저장
    with open(temp_file_path, 'w') as file:
        file.write(code)

    try:
        # Node.js 스크립트 실행
        process = subprocess.run(['node', temp_file_path], input=input_data, text=True, capture_output=True, check=True)
        output = process.stdout.strip()

        # 출력 비교
        result = {
            "error": False,
            "error_message": None,
            "input": input_data,
            "expected_output": expected_output,
            "actual_output": output,
            "correct": output == expected_output
        }
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip() if e.stderr else "Unknown error"
        result = {
            "error": True,
            "error_message": error_message,
            "input": input_data,
            "expected_output": expected_output,
            "actual_output": None,
            "correct": False
        }
    finally:
        # 임시 파일 삭제
        os.remove(temp_file_path)

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
