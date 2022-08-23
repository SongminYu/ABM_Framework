# README

### Next steps

#### before launch

* python版本适配
* Songmin --> tutorial
* Zhanyi --> 生成文档的api reference
  * 写批注
  * 给内置函数加下划线

* agent可以访问self.network
* 以render_building为例，data_collector的时间记录：自定义函数算在了model-run里(加装饰符或删掉分部分计时？)
* create_grid和create_network的默认参数grid_cls, spot_cls...
* 把各种xxx_id改成id_xxx

#### organization page
* library --> papers
* articles in Chinese? (from WeChat)
* discussion platform? --> Discussions at github

#### long-term plan

* trainer和calibrator有可以抽象共用的东西
* 过一遍visualizer需要的功能 --> 讲课可以没有
* 一个项目模板 -- 文件夹结构、gitignore 
* tralibrator

[![Build status](https://app.travis-ci.com/SongminYu/Melodie.svg?token=qNTghqDqnwadzvj4y4z7&branch=master&status=passed)](https://travis-ci.com/SongminYu)

This project is supposed to be developed as a general framework that can be used to establish agent-based models for
specific uses. Current main contributors are **Songmin YU** and **Zhanyi HOU**.

### Supported Python Versions

Python from 3.7~3.9

PyPy interpreter is also supported. But Melodie is not designed for PyPy interpreter, so the performance may not be
improved significantly.

### Run this project

```shell
git clone xxxx
pip install Cython pytest
python.exe setup.py build_ext --inplace
pytest
```

### Build docs

```shell
cd docs
sphinx-autobuild source build/html
# click the link appeared in the console to view the documentation website.
```

As for auto-generated API Documentation, run this command to update:
```shell
python setup.py build_ext -i
sphinx-build source build/html -E -a
```

### Run examples

examples are at the `examples/` folder.


### Melodie studio

Melodie has an integrated web-based GUI tool for creating new projects and database viewing. you could start it with
this command:

```sh
python -m Melodie studio
```

or if you have created a project, you could use the studio in a Python script:

```python3
import os

from Melodie.studio.main import studio_main
from Melodie import Config

config = Config(
    project_name='DemoProject',
    project_root=os.path.dirname(__file__),
    sqlite_folder='data/sqlite',
    excel_source_folder='data/excel_source',
    output_folder='data/output',
)

studio_main(config)
```

then visit `http://localhost:8089/` with browser

