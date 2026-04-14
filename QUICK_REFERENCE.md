# 🏥 快速参考卡 - ICU 死亡率预测应用

## ⚡ 30 秒启动

```bash
bash launch.sh              # 推荐 - 选择版本
streamlit run mortality_prediction_app.py         # 基础版
streamlit run mortality_prediction_app_advanced.py # 高级版
```

🌐 打开: http://localhost:8501

---

## 📋 8 个参数输入速记

| # | 参数 | 范围 | 单位 | 快速定位 |
|---|------|------|------|---------|
| 1️⃣ | Group | 1-5 | - | 患者分组 (下拉选择) |
| 2️⃣ | DDPLUS | 0-100 | 分 | 生理学评分 |
| 3️⃣ | Age | 0-120 | 岁 | 患者年龄 |
| 4️⃣ | PDW | 0-50 | % | 血小板异质性 |
| 5️⃣ | BUN | 0-200 | mg/dL | 血尿素氮 ↑ |
| 6️⃣ | LDH | 0-2000 | U/L | 细胞损伤标志 ↑ |
| 7️⃣ | ALT | 0-1000 | U/L | 肝脏标志 ↑ |
| 8️⃣ | PT | 0-100 | 秒 | 凝血时间 ↑ |

---

## 🎯 风险分类速查

| 风险等级 | 死亡率 | 符号 | 建议 |
|---------|-------|------|------|
| **低** | < 35% | ✅ 🟢 | 标准护理 |
| **中** | 35-65% | ⚡ 🟡 | 加强监测 |
| **高** | > 65% | ⚠️ 🔴 | 强化干预 |

---

## 🔧 命令速查

### 启动

```bash
# 快速启动
bash launch.sh

# 基础版
streamlit run mortality_prediction_app.py

# 高级版
streamlit run mortality_prediction_app_advanced.py

# 自定义端口
streamlit run app.py --server.port 8502
```

### 导入数据

```bash
# CSV 格式检查
head -1 patients.csv
# 应该显示: group,DDPLUS,age,PDW,BUN,LDH,ALT,PT

# 验证数据
wc -l patients.csv  # 显示行数
```

### Python 脚本

```python
from utils import ModelManager

manager = ModelManager('final_model_XGB.pkl')
result = manager.predict(2, 45, 58, 15, 28, 320, 65, 13)
print(f"死亡率: {result['mortality_risk']*100:.1f}%")
```

---

## 📊 基础版 vs 高级版

| 功能 | 基础 | 高级 |
|------|------|------|
| 单患者预测 | ✅ | ✅ |
| 批量处理 | ❌ | ✅ |
| 数据分析 | ❌ | ✅ |
| 导出功能 | 基础 | 完整 |
| 学习曲线 | 🟢 陡 | 🟡 中 |
| 文件大小 | 15KB | 25KB |

---

## 📁 关键文件位置

```
mortality_prediction_app.py          基础版应用 (15 KB)
mortality_prediction_app_advanced.py 高级版应用 (25 KB)
final_model_XGB.pkl                  模型文件 (222 KB) ⭐
utils.py                             工具库 (15 KB)
config.json                          配置文件 (2.4 KB)
sample_patients.csv                  示例数据 (456 B)
requirements.txt                     依赖列表 (96 B)
launch.sh                            启动脚本
```

---

## 🚨 常见错误速解

| 错误 | 原因 | 解决 |
|------|------|------|
| `ModuleNotFoundError` | 未安装依赖 | `pip install -r requirements.txt` |
| `Model file not found` | 模型文件丢失 | 检查文件是否存在 |
| `Port already in use` | 端口被占用 | 改用 `--server.port 8502` |
| `CSV error` | 列名不匹配 | 检查列名大小写 |
| `Connection refused` | 应用未启动 | 重新运行启动命令 |

---

## 📈 快速工作流

### 方案 A: 单患者预测 (2 分钟)
```
1. bash launch.sh
2. 选择基础版
3. 输入参数
4. 点击预测按钮
5. 查看结果 ✓
```

### 方案 B: 批量分析 (10 分钟)
```
1. 准备 CSV 文件
2. bash launch.sh
3. 选择高级版
4. 进入 📊 Batch Analysis
5. 上传 CSV
6. 查看结果报告 ✓
```

### 方案 C: 编程自动化 (30 分钟)
```
1. from utils import ModelManager
2. manager = ModelManager(...)
3. results = manager.batch_predict(df)
4. ReportGenerator.export_to_html(...)
5. 获得报告 ✓
```

---

## 📚 文档导航

### 根据你的需求:

**"我是初学者"** → README.md  
**"我需要使用说明"** → USAGE_GUIDE.md  
**"我用高级版"** → ADVANCED_GUIDE.md  
**"我要云端部署"** → DEPLOYMENT.md  
**"我要选择版本"** → VERSION_COMPARISON.md  
**"我要完整指南"** → COMPLETE_GUIDE.md  
**"我要测试应用"** → TEST_CASES.md  

---

## 🔒 数据隐私清单

- [ ] 使用本地环境运行（无云传输）
- [ ] 定期清除历史数据
- [ ] 不上传真实患者姓名
- [ ] 遵守 HIPAA 要求
- [ ] 加密敏感信息存储

---

## 🎓 快速学习

### 5 分钟了解
- [ ] 阅读本快速参考
- [ ] 运行应用一次
- [ ] 输入示例数据
- [ ] 查看预测结果

### 30 分钟掌握
- [ ] 理解 8 个参数含义
- [ ] 学习风险分类规则
- [ ] 尝试不同的输入组合
- [ ] 理解临床建议

### 2 小时精通
- [ ] 完整阅读 USAGE_GUIDE
- [ ] 尝试高级版功能
- [ ] 导出和分析数据
- [ ] 理解底层算法

---

## 💻 快速部署

### 本地运行（推荐新手）
```bash
bash launch.sh  # 选择版本
```

### 局域网共享（推荐团队）
```bash
streamlit run app.py --server.address 0.0.0.0
# 其他机器访问: http://你的IP:8501
```

### 云端部署（推荐生产）
```bash
# 推荐: Streamlit Cloud (完全免费)
# 步骤: GitHub → https://streamlit.io/cloud → 部署
```

---

## 📊 典型场景所需时间

| 场景 | 准备 | 运行 | 结果 | 总计 |
|------|------|------|------|------|
| 单患者预测 | 1m | 0.1m | 0.5m | **1.6m** |
| 5 患者预测 | 2m | 0.5m | 1m | **3.5m** |
| 100 患者批处理 | 5m | 5m | 2m | **12m** |
| 生成详细报告 | 5m | 5m | 3m | **13m** |

---

## 🆘 紧急求助

### 问题解决流程

1. **应用无法启动?**
   ```
   Step 1: python3 --version  (检查 Python)
   Step 2: pip list           (检查依赖)
   Step 3: 重新运行 launch.sh (尝试重启)
   ```

2. **预测结果异常?**
   ```
   Step 1: 检查输入值范围 (见快速参考)
   Step 2: 对比测试用例 (TEST_CASES.md)
   Step 3: 重新输入数据 (排除输入错误)
   ```

3. **批处理失败?**
   ```
   Step 1: 检查 CSV 格式 (列名和数据类型)
   Step 2: 测试小文件 (排除大文件问题)
   Step 3: 查看错误信息 (寻找具体原因)
   ```

### 获取帮助
- 📖 查阅对应文档
- 🔍 搜索关键词 (Ctrl+F)
- 🧪 查看测试用例
- 💬 查阅常见问题

---

## ⚡ 性能优化建议

### 快速响应
```bash
# 使用基础版 (更轻量)
streamlit run mortality_prediction_app.py
```

### 减少延迟
```bash
# 关闭不必要的图表
# 使用小批量数据
# 清除浏览器缓存
```

### 大规模处理
```python
# 使用编程接口
from utils import ModelManager
# 避免 Web 界面的开销
```

---

## 🎯 最常用命令

```bash
# 启动基础版
streamlit run mortality_prediction_app.py

# 启动高级版
streamlit run mortality_prediction_app_advanced.py

# 打开 Python 交互
python3 -c "from utils import ModelManager; print('OK')"

# 查看文件
ls -la *.py *.pkl *.csv

# 清理缓存
rm -rf .streamlit ~/.streamlit
```

---

## 📞 快速链接

| 资源 | 链接 | 说明 |
|------|------|------|
| Streamlit 文档 | streamlit.io/docs | 官方文档 |
| XGBoost 文档 | xgboost.readthedocs.io | 模型文档 |
| Python 官网 | python.org | 编程语言 |
| GitHub | github.com | 代码仓库 |

---

## ✅ 使用前检查清单

- [ ] Python 3.8+ 已安装
- [ ] requirements.txt 已安装
- [ ] final_model_XGB.pkl 文件存在
- [ ] 应用文件完整
- [ ] 可以成功启动应用
- [ ] 可以成功进行单个预测

---

**版本:** v1.1  
**最后更新:** 2024-04-14  
**快速参考卡 - 打印版本合适**

---

## 💡 记忆技巧

**8 个参数记忆法:**
```
你要知道 = Group
病人有多严重 = DDPLUS  
他多少岁 = Age
血小板怎样 = PDW
血尿素多少 = BUN
肝酶高不高 = LDH + ALT
凝血正常否 = PT
```

**风险记忆法:**
```
✅ 低 < 35% (绿灯 - 继续)
⚡ 中 35-65% (黄灯 - 谨慎)
⚠️ 高 > 65% (红灯 - 停止普通护理)
```

---

**祝您使用愉快！** 🏥
