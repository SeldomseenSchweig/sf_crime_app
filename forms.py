from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length



class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')
    location = SelectField('Location', choices=[
    ('All', 'All'),
    ('Mission', 'Mission'), 
    ('South of Market', 'South of Market'), 
    ('Tenderloin', 'Tenderloin'), 
    ('Hayes Valley', 'Hayes Valley'),
    ('Excelsior', 'Excelsior'),
    ('North Beach', 'North Beach'), 
    ('Financial District/South Beach', 'Financial District/South Beach'), 
    ('Bayview Hunters Point', 'Bayview Hunters Point'), 
    ('Japantown', 'Japantown'),
    ('Pacific Heights', 'Pacific Heights'),
    ('Noe Valley', 'Noe Valley'),
    ('Nob Hill', 'Nob Hill'),
    ('Visitacion Valley', 'Visitacion Valley'),
    ('Lone Mountain/USF', 'Lone Mountain/USF'),
    ('Marina', 'Marina'),
    ('Inner Sunset', 'Inner Sunset'),
    ('Outer Mission', 'Outer Mission'),
    ('Haight Ashbury', 'Haight Ashbury'),
    ('Portola', 'Portola'),
    ('Outer Richmond', 'Outer Richmond'),
    ('West of Twin Peaks', 'West of Twin Peaks'),
    ('Chinatown', 'Chinatown'),
    ('Presidio', 'Presidio'),
    ('Castro/Upper Market', 'Castro/Upper Market'),
    ('Russian Hill', 'Russian Hill'),
    ('Sunset/Parkside', 'Sunset/Parkside'),
    ('Seacliff', 'Seacliff'),
    ('Oceanview/Merced/Ingleside', 'Oceanview/Merced/Ingleside'),
    ('Western Addition', 'Western Addition'),
    ('Mission Bay', 'Mission Bay')])




class UserEditForm(FlaskForm):
    """Form for editing users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Image URL')
    header_image_url= StringField('(Optional) Image URL')
    password = PasswordField('Password', validators=[Length(min=6)])
    location = SelectField('Location', choices=[
    ('All', 'All'),
    ('Mission', 'Mission'), 
    ('South of Market', 'South of Market'), 
    ('Tenderloin', 'Tenderloin'), 
    ('Hayes Valley', 'Hayes Valley'),
    ('Excelsior', 'Excelsior'),
    ('North Beach', 'North Beach'), 
    ('Financial District/South Beach', 'Financial District/South Beach'), 
    ('Bayview Hunters Point', 'Bayview Hunters Point'), 
    ('Japantown', 'Japantown'),
    ('Pacific Heights', 'Pacific Heights'),
    ('Noe Valley', 'Noe Valley'),
    ('Nob Hill', 'Nob Hill'),
    ('Visitacion Valley', 'Visitacion Valley'),
    ('Lone Mountain/USF', 'Lone Mountain/USF'),
    ('Marina', 'Marina'),
    ('Inner Sunset', 'Inner Sunset'),
    ('Outer Mission', 'Outer Mission'),
    ('Haight Ashbury', 'Haight Ashbury'),
    ('Portola', 'Portola'),
    ('Outer Richmond', 'Outer Richmond'),
    ('West of Twin Peaks', 'West of Twin Peaks'),
    ('Chinatown', 'Chinatown'),
    ('Presidio', 'Presidio'),
    ('Castro/Upper Market', 'Castro/Upper Market'),
    ('Russian Hill', 'Russian Hill'),
    ('Sunset/Parkside', 'Sunset/Parkside'),
    ('Seacliff', 'Seacliff'),
    ('Oceanview/Merced/Ingleside', 'Oceanview/Merced/Ingleside'),
    ('Western Addition', 'Western Addition'),
    ('Mission Bay', 'Mission Bay'),('Glen Park', 'Glen Park'),
    ('Presidio Heights', 'Presidio Heights'),
    ('Golden Gate Park', 'Golden Gate Park'),
    ('Lakeshore', 'Lakeshore'),
    ('McLaren Park', 'McLaren Park'),
    ('Lincoln Park', 'Lincoln Park'),
    ('Treasure Island', 'Treasure Island'),
    ('Twin Peaks', 'Twin Peaks')])



class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])




class NewHoodWatchForm(FlaskForm):
    """ Form for looking at a new neighborhood """
    location = SelectField('Location', choices=[('All', 'All'),
    ('Mission', 'Mission'), 
    ('South of Market', 'South of Market'), 
    ('Tenderloin', 'Tenderloin'), 
    ('Hayes Valley', 'Hayes Valley'),
    ('Excelsior', 'Excelsior'),
    ('North Beach', 'North Beach'), 
    ('Financial District/South Beach', 'Financial District/South Beach'), 
    ('Bayview Hunters Point', 'Bayview Hunters Point'), 
    ('Japantown', 'Japantown'),
    ('Pacific Heights', 'Pacific Heights'),
    ('Noe Valley', 'Noe Valley'),
    ('Nob Hill', 'Nob Hill'),
    ('Visitacion Valley', 'Visitacion Valley'),
    ('Lone Mountain/USF', 'Lone Mountain/USF'),
    ('Marina', 'Marina'),
    ('Inner Sunset', 'Inner Sunset'),
    ('Outer Mission', 'Outer Mission'),
    ('Haight Ashbury', 'Haight Ashbury'),
    ('Portola', 'Portola'),
    ('Outer Richmond', 'Outer Richmond'),
    ('West of Twin Peaks', 'West of Twin Peaks'),
    ('Chinatown', 'Chinatown'),
    ('Presidio', 'Presidio'),
    ('Castro/Upper Market', 'Castro/Upper Market'),
    ('Russian Hill', 'Russian Hill'),
    ('Sunset/Parkside', 'Sunset/Parkside'),
    ('Seacliff', 'Seacliff'),
    ('Oceanview/Merced/Ingleside', 'Oceanview/Merced/Ingleside'),
    ('Western Addition', 'Western Addition'),
    ('Mission Bay', 'Mission Bay'),
    ('Glen Park', 'Glen Park'),
    ('Presidio Heights', 'Presidio Heights'),
    ('Golden Gate Park', 'Golden Gate Park'),
    ('Lakeshore', 'Lakeshore'),
    ('McLaren Park', 'McLaren Park'),
    ('Lincoln Park', 'Lincoln Park'),
    ('Treasure Island', 'Treasure Island'),
    ('Twin Peaks', 'Twin Peaks')])
    
    crime_description = SelectField('Crime Description',
    choices=[('All', 'All'),('Vehicle Impounded', 'Vehicle Impounded'),
    ('Suicide', 'Suicide'),
    ('Vehicle Misplaced', 'Vehicle Misplaced'),
    ('Drug Violation', 'Drug Violation'),
    ('Rape', 'Rape'),
    ('Human Trafficking (A), Commercial Sex Acts', 'Human Trafficking (A), Commercial Sex Acts'),
    ('Suspicious', 'Suspicious'),
    ('Homicide', 'Homicide'),
    ('Motor Vehicle Theft', 'Motor Vehicle Theft'),
    ('Liquor Laws', 'Liquor Laws'),
    ('Gambling', 'Gambling'),
    ('Weapons Offence', 'Weapons Offence'),
    ('Case Closure', 'Case Closure'),
    ('Forgery And Counterfeiting', 'Forgery And Counterfeiting'),
    ('Courtesy Report', 'Courtesy Report'),
    ('Arson', 'Arson'),
    ('Traffic Collision', 'Traffic Collision'),
    ('Vandalism', 'Vandalism'),
    ('Prostitution', 'Prostitution'),
    ('Fire Report', 'Fire Report'),
    ('Civil Sidewalks', 'Civil Sidewalks'),
    ('Embezzlement', 'Embezzlement'),
    ('Sex Offense', 'Sex Offense'),
    ('Robbery', 'Robbery'),
    ('Missing Person', 'Missing Person'),
    ('Suspicious Occ', 'Suspicious Occ'),
    ('Disorderly Conduct', 'Disorderly Conduct'),
    ('Offences Against The Family And Children', 'Offences Against The Family And Children'),
    ('Traffic Violation Arrest', 'Traffic Violation Arrest'),
    ('Miscellaneous Investigation', 'Miscellaneous Investigation'),
    ('Other Offenses', 'Other Offenses'),
    ('Weapons Offense', 'Weapons Offense'),
    ('Weapons Carrying Etc', 'Weapons Carrying Etc'),
    ('Stolen Property', 'Stolen Property'),
    ('Drug Offense', 'Drug Offense'),
    ('Lost Property', 'Lost Property'),
    ('Warrant', 'Warrant'),
    ('Fraud', 'Fraud'),
    ('Recovered Vehicle', 'Recovered Vehicle'),
    ('Motor Vehicle Theft', 'Motor Vehicle Theft'),
    ('Burglary', 'Burglary'),
    ('Non-Criminal', 'Non-Criminal'),
    ('Assault', 'Assault'),
    ('Malicious Mischief', 'Malicious Mischief'),
    ('Other Miscellaneous', 'Other Miscellaneous'),
    ('Larceny Theft', 'Larceny Theft'),
    ('Human Trafficking (B), Involuntary Servitude', 'Human Trafficking (B), Involuntary Servitude'),
    ('Human Trafficking, Commercial Sex Acts', 'Human Trafficking, Commercial Sex Acts')]
    )
    date = DateField("DD-MM-YYYY - Date after 2017",format='%m/%d/%Y' )
