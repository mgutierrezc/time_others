(function () {
    'use strict';

    $(document).ready(function () {
        var selector = '[data-slider] input[type="range"]';
        var setSliderValue = function () {
            var $input = $(this),
                $slider = $input.closest('[data-slider]'),
                $valueTarget = $slider.find('[data-slider-value]'),
                value = $input.val();
            $valueTarget.text(value);
        };

        $(selector).each(setSliderValue);
        $(document).on('change input', selector,setSliderValue);
        // block the user from spamming the next button which can make congestion
        // problems worse.
        // i can't use $('.otree-btn-next').click()
        // because disabling the button inside the handler interferes with form
        // submission.
        $('#form').submit(function () {
            $('.otree-btn-next').each(function() {
                let nextButton = this;
                let originalState = nextButton.disabled;
                nextButton.disabled = true;
                setTimeout(function() {
                    // restore original state.
                    // it's possible the button was disabled in the first place?
                   nextButton.disabled = originalState;
                }, 15000);
            });
        });
    });
})();
