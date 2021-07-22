function validateForm()
{
    var username=document.getElementById('username').value
    var pwd=document.getElementById('password').value
    var cpwd=document.getElementById('confirmpassword').value
    var pattern = new RegExp("[a-zA-Z]{1}[a-zA-Z0-9_]{2,}")
    if(pattern.test(username))
    {
        pattern=new RegExp("[a-zA-Z]{1}[a-zA-Z0-9_@#$&]{2,}")
        if(pattern.test(pwd))
        {
            if(pwd!=cpwd)
            {
                window.alert('Password and confirm password does not match')
                return false
            }
            else
            {
                return true
            }
        }
        else
        {
            window.alert('Password should start with a-z or A-Z and can contain @,#,$,&,_')
            return false
        }
    }
    else
    {
        window.alert('Username should start with a-z or A-Z and can contain a-z,A-Z,0-9,_ and should be minimum of 3 characters')
        return false
    }
}
