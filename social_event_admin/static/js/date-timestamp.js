$(document).ready(function() {
    $("form").on("submit", function() {
        $(".input-group.date").each(function(index, element) {
            let $input = $(element).find("input")
            let timestr = $input.val()
            let date = new Date(timestr)
            let timestamp = (date - new Date('1970-01-01')) / 1000
            $input.val(timestamp)
        })
    })

    $(".input-group.date").each(function(index, element) {
        let $input = $(element).find("input")
        let timestamp = $input.val()
        var date = new Date('1970-01-01')
        date.setSeconds(parseInt(timestamp) || 0)
        $input.val(date.toJSON().substring(0, 19))
    })
})
