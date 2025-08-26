from datetime import date, timedelta, datetime

from logging.handlers import TimedRotatingFileHandler


class DateRangeTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, base_filename, start_date, end_date, *args, **kwargs):
        self.base_filename = base_filename
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self.current_week_start = self.start_date
        self.current_week_end = self._get_week_end(self.current_week_start)
        self._validate_dates()
        self.filename = self._get_weekly_filename()
        super().__init__(self.filename, *args, **kwargs)

    def _get_week_end(self, start_date):
        return start_date + timedelta(days=(6 - start_date.weekday()))

    def _validate_dates(self):
        if self.end_date <= self.start_date:
            raise ValueError("End date must be after start date")

    def _get_weekly_filename(self):    
        today = date.today()

        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        start_date_str = start_of_week.strftime('%Y-%m-%d')
        end_date_str = end_of_week.strftime('%Y-%m-%d')
            
        return f"{self.base_filename}_{start_date_str}_to_{end_date_str}.log"
    
    def doRollover(self):
        self.current_week_start = self.current_week_start + timedelta(weeks=1)
        self.current_week_end = self._get_week_end(self.current_week_start)
        self.filename = self._get_weekly_filename()
        super().doRollover()
