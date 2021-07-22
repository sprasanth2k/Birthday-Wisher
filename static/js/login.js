function showPassword()
{
    if(document.getElementById("showpassword").checked==true)
    {
        document.getElementById('password').type="text"
    }
    else
    {
        document.getElementById('password').type="password"
    }    
}