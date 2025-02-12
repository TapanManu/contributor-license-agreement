# The line is of the format "+| `full name`| [gitLogin](https://github.com/gitLogin) |12-july-2021|"
from os import error
from datetime import date

months = ["january","february","march","april","may","june","july",
            "august","september","october","november","december"]

# Change line is of the format "+| `full name`| [pr_raiser_login](https://github.com/pr_raiser_login) |12-july-2021|"



def valid_date(Date):
    try:
        print("*")
        day,month,year = Date.split('-')
        print(year,month,day)
        login_day = date(int(year),months.index(month.lower())+1,int(day))
    except :
        print("**")
        return False
    else:
        print("***")
        today = date.today()
        diff = today - login_day
        if(diff.days > 7):
            return False
    
    return True

def validate_change(pr_raiser_login, change):
    personal_cla_file = 'personal_contributor_licence_agreement.md'
    employer_cla_file = 'employer_contributor_license_agreement.md'
    # validation code here
    
    user_start =  change.find('[')
    user_end = change.find(']')

    

    login_user = change[user_start+1:user_end]

    github_user_start = github_user_end = -1
    for i in range(0,1):
        github_user_end = change.find(')',github_user_end+1)
    for _ in range(0,3):
        github_user_start = change.find('/',github_user_start+1)

    user_name = change[github_user_start+1:github_user_end]

    full_name_loc = change.find('|')
    full_name_loc_next = change.find('|',full_name_loc+1)

    full_name = change[full_name_loc+2:full_name_loc_next] 

    # compare dates
    date_start = change.find('|',full_name_loc_next+1)
    date_end = change.find('|',date_start+1)
    Date = change[date_start+1:date_end] 

    #********************************************

    if change[1]!= '|' or change[user_start-2]!='|':
         # valid row format
         valid_row = "+| `full name`| ["+pr_raiser_login+"](https://github.com/"+pr_raiser_login+") |"+Date+"|"
         # not syncing with DateERROR ,if this goes correct, DATEERROR COMES up or vice versa ,hence alternative chosen
         return EXPECTED_ERROR_MESSAGE

    

    
    

    if full_name != "`full name`":
        return EXPECTED_ERROR_MESSAGE + "please use `full name` instead of 'full name'"
    if(pr_raiser_login != login_user):
        return EXPECTED_ERROR_MESSAGE + 'Github username should be same as pull request user name'
    if(pr_raiser_login != user_name):
        return EXPECTED_ERROR_MESSAGE + 'Github username should be same as pull request user name'

    if not valid_date(Date):
        return DATE_ERROR_MESSAGE

    

    return True

# user names should be valid

EXPECTED_ERROR_MESSAGE = "Error: The expected line should be: | `full name` | [naren](https://github.com/naren) | 14-july-2021 | \n"
assert validate_change('naren', "+| `full name`| [some_wrong_user](https://github.com/naren) |14-july-2021|") == EXPECTED_ERROR_MESSAGE + 'Github username should be same as pull request user name'
assert validate_change('naren', "+| `full name`| [naren](https://github.com/some_wrong_user) |14-july-2021|") == EXPECTED_ERROR_MESSAGE + 'Github username should be same as pull request user name'
assert validate_change('naren', "+| 'full name'| [naren](https://github.com/some_wrong_user) |14-july-2021|") == EXPECTED_ERROR_MESSAGE + "please use `full name` instead of 'full name'"

# Date should be within one week of today and should be of the format dd-month-YYYY
DATE_ERROR_MESSAGE = EXPECTED_ERROR_MESSAGE + "Invalid date: date should be within one week of <today's date in dd-month-YYYY format>"
assert validate_change('naren', "+| `full name`| [naren](https://github.com/naren) |14-july-2020|") == DATE_ERROR_MESSAGE
assert validate_change('naren', "+| `full name`| [naren](https://github.com/naren) |14-06-2021|") == DATE_ERROR_MESSAGE
assert validate_change('naren', "+| `full name`| [naren](https://github.com/naren) ||") == DATE_ERROR_MESSAGE

# Invalid row fomatting
EXPECTED_ERROR_MESSAGE = "Error, invalid row format: The expected line should be: +| `full name`| [naren](https://github.com/naren) |14-july-2021| \n"
assert validate_change('naren', "+ `full name`| [naren](https://github.com/naren) |25-july-2021|") == EXPECTED_ERROR_MESSAGE
assert validate_change('naren', "lols") == EXPECTED_ERROR_MESSAGE
assert validate_change('naren', "+| `full name` [naren](https://github.com/naren) |25-july-2021|") == EXPECTED_ERROR_MESSAGE
assert validate_change('naren', "+ `full name`| [nare") == EXPECTED_ERROR_MESSAGE
assert validate_change('naren', "+       | `full name`|   [naren](https://github.com/naren)  |25-july-2021  |   ") == EXPECTED_ERROR_MESSAGE + "Please remove extra spaces in the start of the line."

# check if already signed
EXPECTED_ERROR_MESSAGE = "Error,  Njay2000 has already signed the personal contributor license agreement."
assert validate_change('Njay2000', "+| `full name`| [Njay2000](https://github.com/Njay2000) |25-july-2021|") == EXPECTED_ERROR_MESSAGE
EXPECTED_ERROR_MESSAGE = "Error,  mathewdennis1 has already signed the employer contributor license agreement."
assert validate_change('mathewdennis1', "+| `full name`| [mathewdennis1](https://github.com/mathewdennis1) |25-july-2021|") == EXPECTED_ERROR_MESSAGE

# success case
EXPECTED_SUCCESS_MESSAGE = "ok"
assert validate_change('newuser', "+| `full name user` | [newuser](https://github.com/newuser) | 25-july-2021 |") == EXPECTED_SUCCESS_MESSAGE
assert validate_change('newuser', "+|`full name user`|[newuser](https://github.com/newuser)|25-july-2021|") == EXPECTED_SUCCESS_MESSAGE
assert validate_change('newuser', "+|  `full name user`   |    [newuser](https://github.com/newuser)   |  25-july-2021  |") == EXPECTED_SUCCESS_MESSAGE

print("success")
