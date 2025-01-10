**Initialization:** Enter the `VirusFactor` directory and start the `setup` program.

```bash
bash setup/setup.sh
```

Please enter your MySQL username and password as prompted, and check if the dependencies have been installed successfully.

**Set Environment Variable:** <font color='red'>Replace `your_password`  </font>with your MySQL password and enter the following command.

```bash
export DATABASE_URI='mysql+pymysql://root:your_password@localhost/VirusFactor?charset=utf8mb4'
```

**Start the Web Page:** Run the application script `app.py`.

```bash
python3 web/app.py
```

Open your browser and visit `http://127.0.0.1:5000` to use the web application.


