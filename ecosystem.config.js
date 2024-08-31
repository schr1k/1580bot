module.exports = {
    apps: [
        {
            name: "1580",
            script: "source venv/bin/activate && pip install -r requirements.txt && python3.12 main.py",
            time: true,
            log_date_format: "DD.MM.YYYY HH:mm:ss"
        }
    ]
}