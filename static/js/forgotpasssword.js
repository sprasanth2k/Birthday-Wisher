function validateForm()
{
    var pwd=document.getElementById('password').value
    var cpwd=document.getElementById('confirmpassword').value
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