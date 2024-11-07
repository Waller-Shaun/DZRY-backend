const express = require('express');
const { spawn } = require('child_process');

const app = express();
const PORT = 3000;

app.use(express.json()); // 解析 JSON 请求

app.post('/process', (req, res) => {
  console.log("Received a request to /process"); // 打印日志

  const input = req.body.input; // 从请求中获取输入内容
  console.log(input); // 打印日志
  // 使用 child_process 运行 Python 主文件
  const pythonProcess = spawn('python', [".\\py_algorithm\\问题与回答\\问答机器人.py", input]);

  // 捕获 Python 脚本的输出
  let result = '';
  pythonProcess.stdout.on('data', (data) => {
    result += data.toString('utf8');
  });

  // 捕获 Python 脚本的错误输出
  pythonProcess.stderr.on('data', (data) => {
    console.error('Error:', data.toString());
  });

  // 当 Python 脚本执行结束时，发送响应
  pythonProcess.on('close', (code) => {
    result = result.replace(/\r?\n/g, '');
    res.send({ result });
  });
});

app.get('/', (req, res) => {
  res.send('Hello, Neo4j!');
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
