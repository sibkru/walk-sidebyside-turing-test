jsPsych.plugins['training'] = (function() {
    var plugin = {};

    plugin.info = {
        name: 'training',
        parameters: {
            stimulus: {
                type: jsPsych.plugins.parameterType.STRING,
                pretty_name: 'filename',
                default: null,
                description: 'filename.'
            }
        },
        choices: {
            type: jsPsych.plugins.parameterType.KEYCODE,
            pretty_name: 'Choices',
            array: true,
            default: jsPsych.ALL_KEYS,
            description: 'The keys the subject is allowed to press to respond to the stimulus.'
        },
    }

    plugin.trial = function(display_element, trial){
        var then = performance.now()*0.001;
        var left_lines  = trial_txt_to_array(trainLeft);
        var right_lines = trial_txt_to_array(trainRight);
        
        // implement same trial length
       
        function slice_frames(){
            var l = left_lines.length - 1;
            var r = right_lines.length - 1;
            if (l > r){
                left_lines = left_lines.slice(0, r);
                right_lines = right_lines.slice(0, r);
            } else {
                left_lines = left_lines.slice(0, l);
                right_lines = right_lines.slice(0, l);
        }};
        slice_frames();
        var T = Math.max(left_lines.length, right_lines.length) / 24 * 1000;
        console.log(left_lines, right_lines);
        main(left_lines, '#glcanvas_l', then); // corrected right to left
        main(right_lines, '#glcanvas_r', then);
        jsPsych.pluginAPI.setTimeout(function() {
            jsPsych.finishTrial();
        }, T);
    }
    return plugin;
})();