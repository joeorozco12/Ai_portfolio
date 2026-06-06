function y = lookup_forward_voltage_vs_forward_current(x)
% [SYNTHETIC — FOR DEMONSTRATION ONLY]
% Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.
% Curve: forward_voltage_vs_forward_current
% Source: synthetic_datasheet_style_plot, page synthetic_page_20
% Note: Reference-only synthetic plot data. Not guaranteed by a manufacturer. Engineer review is required before use as WCCA or feasibility input.
% Warning: Do not use for WCCA, feasibility, thermal, optical, design-review, or design-decision workflows until qualified engineering review is complete.
% Warning: This lookup clamps outside the digitized x-range and is not an approved extrapolation model.

segments = [
    2.8 2.95 50 100 5513.51351351 -11571.5715716
    2.95 3.1 150 972.972972973 6650.55643879 -7580.28616852
    3.1 3.25 420 2456.47058824 16385.9477124 -46564.2701525
    3.25 3.4 1000 4229.16666667 3759.25925926 -5617.28395062
    3.4 3.55 1700 4977.77777778 4740.74074074 -15802.4691358
    3.55 3.7 2500 5333.33333333 5079.36507936 -33862.4338624
    3.7 3.85 3300 4571.42857143 -3174.6031746 -4232.8042328
];

y = zeros(size(x));
for idx = 1:numel(x)
    x_value = x(idx);
    if x_value <= segments(1, 1)
        y(idx) = segments(1, 3);
    elseif x_value >= segments(end, 2)
        t = segments(end, 2) - segments(end, 1);
        y(idx) = segments(end, 3) + segments(end, 4) * t + segments(end, 5) * t^2 + segments(end, 6) * t^3;
    else
        for seg_idx = 1:size(segments, 1)
            if x_value >= segments(seg_idx, 1) && x_value <= segments(seg_idx, 2)
                t = x_value - segments(seg_idx, 1);
                y(idx) = segments(seg_idx, 3) + segments(seg_idx, 4) * t + segments(seg_idx, 5) * t^2 + segments(seg_idx, 6) * t^3;
                break;
            end
        end
    end
end
end
