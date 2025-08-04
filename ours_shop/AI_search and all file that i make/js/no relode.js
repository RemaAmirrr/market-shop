function GetData()
{
  $.ajax({
    type: "POST",
    url: "http://" + window.location.host + "/readAsk",
    data: $(".frm-getdata").serialize(),
    beforeSend: function() {
        $(".wite").html("درحال دریافت.....");
    },
    success: function(result)
    {
        
        $(".wite").html("")
        obj = JSON.parse(result);
        if(obj.length>0)
        {
            trstr="";
            for (item in obj)
            {
                trstr=trstr+"<tr> <td>"+obj[itme]["fields"]["title"]+"</td>"+
                " <td>"+obj[item]["fields"]["cation"]+"</td>"+
                " <td>"+obj[item]["fields"]["Created"]+"</td>"+
                "<td>"+
                "<button type='button' class='btn btn-primar ' "+
                "onclick='Setdates(\""+obj[item]["fields"]["title"]+"\", \""+obj[item]["fields"]["caption"]+ "\",\""+obj[item]["fields"]["id"]+" \")'"+
                "data-toggle='model' data-target='#myModal'>ویرایش </button> </td> "

                +"<button type='button' class='btn btn-danger' "+
                "onclick=' $(\".id\").val(\""+obj[item]["pk"]+"\");  '"+
                "data-toggle='modal' data-target='#myModalDelet'>حزف</button> </td> "
                +" <tr>";
          
            }
            $(".body-table").html(trstr);

        }   
        else
        {
            $(".wite").html("اطلاعاتی برای نمایش وجود ندارد");
        } 
    },
  })
}