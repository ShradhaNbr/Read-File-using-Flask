from flask import Flask, render_template, request
import chardet

app = Flask(__name__)

@app.route('/', defaults={'filename':'file1.txt'})
@app.route('/<filename>')
def read_file(filename):
    start_line = request.args.get('start_line')
    end_line = request.args.get('end_line')
    try:
        with open(filename,'rb') as f:
            result = chardet.detect(f.read())
            encoding=result['encoding']
        with open(filename,'r', encoding=encoding) as f:
            lines = f.readlines()
            if start_line and end_line:
                start_line = int(start_line)
                end_line = int(end_line)
                lines = lines[start_line-1:end_line]
                print(lines)
            elif start_line:
                start_line = int(start_line)
                lines = lines[start_line-1:]
            elif end_line:
                end_line = int(end_line)
                lines = lines[:end_line]
            
            content = ''.join(lines)

            return render_template('file.html', content=content)
    
    except Exception as e:
        return render_template('error.html', error=str(e))
    
if __name__ == '__main__':
    app.run()
