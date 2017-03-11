$(document).ready(function() {
    $(".input-group.date").each(function(index, element) {
        let $input = $(element).find("input")
        let timestamp = $input.val()
        var date = new Date('1970-01-01')
        date.setSeconds(parseInt(timestamp))
        $input.val(date.toJSON().substring(0, 19))
    })

    $("form").on("submit", function() {
        $(".input-group.date").each(function(index, element) {
            let $input = $(element).find("input")
            let timestr = $input.val()
            let date = new Date(timestr)
            let timestamp = (date - new Date('1970-01-01')) / 1000
            $input.val(timestamp)
        })
    })
})
