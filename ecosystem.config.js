module.exports = {
    apps: [
        {
            name: "1580",
            script: "python3.11 main.py",
            out_file: "./pm2/out.log",
            error_file: "./pm2/error.log",
            time: true,
            log_date_format: "DD.MM.YYYY HH:mm:ss"
        }
    ]
}