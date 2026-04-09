"""Manim animations for Post 1: What Gradients Actually Tell a Model.

Scenes:
  - UpdateRuleDissected: Build the update equation piece by piece, each symbol lights up
  - GradientParliament: Per-sample gradient arrows merge into resultant
  - GradientWeathervane: Remove one data point, watch gradient rotate
"""

from manim import *
import numpy as np


# ──────────────────────────────────────────────
# Color palette
# ──────────────────────────────────────────────
COLORS = [BLUE, GREEN, ORANGE, PURPLE, RED]
BG_COLOR = "#1a1a2e"
ACCENT = YELLOW
SOFT_WHITE = "#e0e0e0"


class UpdateRuleDissected(Scene):
    """Build theta_{t+1} = theta_t - eta * nabla L piece by piece.
    Each symbol lights up with its physical meaning."""

    def construct(self):
        self.camera.background_color = BG_COLOR

        # The full equation (start dimmed)
        equation = MathTex(
            r"\theta_{t+1}", "=", r"\theta_t", "-", r"\eta",
            r"\nabla_\theta", r"\mathcal{L}", r"(\theta_t)",
            font_size=60,
        )
        equation.set_color(GREY_D)
        equation.move_to(UP * 1.5)

        self.play(Write(equation), run_time=1.5)
        self.wait(0.5)

        # ── theta_t: "Where you are now" ──
        label_pos = Text(
            "Where you are now", font_size=28, color=SOFT_WHITE
        ).next_to(equation, DOWN, buff=1.0)

        self.play(
            equation[2].animate.set_color(BLUE),
            FadeIn(label_pos, shift=UP * 0.3),
            run_time=0.8,
        )
        self.wait(1.2)
        self.play(FadeOut(label_pos), run_time=0.4)

        # ── nabla L: "What the data is telling you" ──
        label_grad = Text(
            "What the data is telling you", font_size=28, color=SOFT_WHITE
        ).next_to(equation, DOWN, buff=1.0)

        self.play(
            equation[5].animate.set_color(RED),
            equation[6].animate.set_color(RED),
            equation[7].animate.set_color(RED),
            FadeIn(label_grad, shift=UP * 0.3),
            run_time=0.8,
        )
        self.wait(1.5)
        self.play(FadeOut(label_grad), run_time=0.4)

        # ── eta: "How much you trust that opinion" ──
        label_lr = Text(
            "How much you trust that opinion", font_size=28, color=SOFT_WHITE
        ).next_to(equation, DOWN, buff=1.0)

        self.play(
            equation[4].animate.set_color(GREEN),
            FadeIn(label_lr, shift=UP * 0.3),
            run_time=0.8,
        )
        self.wait(1.5)
        self.play(FadeOut(label_lr), run_time=0.4)

        # ── minus sign: "Go the other way" ──
        label_minus = Text(
            "Go the other way — downhill", font_size=28, color=SOFT_WHITE
        ).next_to(equation, DOWN, buff=1.0)

        self.play(
            equation[3].animate.set_color(YELLOW),
            FadeIn(label_minus, shift=UP * 0.3),
            run_time=0.8,
        )
        self.wait(1.2)
        self.play(FadeOut(label_minus), run_time=0.4)

        # ── theta_{t+1}: the result ──
        label_result = Text(
            "Where you end up", font_size=28, color=SOFT_WHITE
        ).next_to(equation, DOWN, buff=1.0)

        self.play(
            equation[0].animate.set_color(TEAL),
            equation[1].animate.set_color(SOFT_WHITE),
            FadeIn(label_result, shift=UP * 0.3),
            run_time=0.8,
        )
        self.wait(1.0)
        self.play(FadeOut(label_result), run_time=0.4)

        # ── Summary line ──
        summary = Text(
            "New position = old position − trust × data's opinion",
            font_size=26,
            color=ACCENT,
        ).next_to(equation, DOWN, buff=1.2)

        self.play(FadeIn(summary, shift=UP * 0.3), run_time=0.8)
        self.wait(2.0)

        # ── Animate a few descent steps on a 1D curve ──
        self.play(
            FadeOut(equation), FadeOut(summary),
            run_time=0.6,
        )

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 5, 1],
            x_length=8,
            y_length=4,
            axis_config={"color": GREY_B, "include_tip": False},
        ).shift(DOWN * 0.3)

        loss_curve = axes.plot(
            lambda x: 0.4 * x**4 - 1.5 * x**2 + 2.5,
            color=BLUE_C,
            x_range=[-2.5, 2.5],
        )
        loss_label = axes.get_axis_labels(
            x_label=MathTex(r"\theta", color=SOFT_WHITE),
            y_label=MathTex(r"\mathcal{L}", color=SOFT_WHITE),
        )

        self.play(
            Create(axes), Create(loss_curve), FadeIn(loss_label),
            run_time=1.0,
        )

        # Descending dot
        x_val = 2.0
        dot = Dot(
            axes.c2p(x_val, 0.4 * x_val**4 - 1.5 * x_val**2 + 2.5),
            color=ACCENT,
            radius=0.1,
        )
        self.play(FadeIn(dot), run_time=0.3)

        lr = 0.08
        for _ in range(12):
            grad = 1.6 * x_val**3 - 3.0 * x_val  # derivative
            x_new = x_val - lr * grad
            y_new = 0.4 * x_new**4 - 1.5 * x_new**2 + 2.5
            self.play(
                dot.animate.move_to(axes.c2p(x_new, y_new)),
                run_time=0.25,
            )
            x_val = x_new

        self.wait(1.5)


class GradientParliament(Scene):
    """Five data points each emit gradient arrows, which merge into a resultant.
    Shows that the gradient is a sum of individual opinions."""

    def construct(self):
        self.camera.background_color = BG_COLOR

        # Title
        title = Text("The Gradient Parliament", font_size=36, color=SOFT_WHITE)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title), run_time=0.6)

        # ── Parameter space (contour background) ──
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=5.5,
            background_line_style={
                "stroke_color": GREY_D,
                "stroke_width": 0.5,
                "stroke_opacity": 0.3,
            },
            axis_config={"stroke_color": GREY_B, "stroke_width": 1},
        ).shift(DOWN * 0.3)

        # Draw some contour ellipses
        contours = VGroup()
        for r in [0.8, 1.5, 2.3, 3.0]:
            ellipse = Ellipse(
                width=r * 2.2, height=r * 1.6,
                color=BLUE_E, stroke_width=1, stroke_opacity=0.3,
            ).shift(plane.c2p(-0.5, -0.3))
            contours.add(ellipse)

        self.play(Create(plane), FadeIn(contours), run_time=0.8)

        # Current parameter point
        param_pos = plane.c2p(1.5, 1.0)
        param_dot = Dot(param_pos, color=WHITE, radius=0.12)
        param_label = MathTex(r"\theta_t", font_size=28, color=WHITE).next_to(
            param_dot, UR, buff=0.15
        )
        self.play(FadeIn(param_dot), FadeIn(param_label), run_time=0.4)

        # ── Data points in sidebar ──
        data_labels = [
            "cat photo",
            "dog photo",
            "blurry cat",
            "rare bird",
            "dog again",
        ]
        # Per-sample gradient directions (in parameter space)
        # The "rare bird" (index 3) has a large, divergent gradient
        grad_vectors = [
            np.array([-0.8, -0.5]),    # cat — moderate, toward minimum
            np.array([-0.6, -0.7]),    # dog — similar to cat
            np.array([-0.5, -0.3]),    # blurry cat — small, roughly same dir
            np.array([-0.3,  1.2]),    # rare bird — LARGE, different direction!
            np.array([-0.7, -0.6]),    # dog again — similar to others
        ]

        sidebar = VGroup()
        for i, (label, color) in enumerate(zip(data_labels, COLORS)):
            dot = Dot(color=color, radius=0.08)
            text = Text(label, font_size=18, color=color)
            row = VGroup(dot, text).arrange(RIGHT, buff=0.15)
            sidebar.add(row)
        sidebar.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        sidebar.to_edge(RIGHT, buff=0.3).shift(DOWN * 0.5)

        self.play(FadeIn(sidebar), run_time=0.6)
        self.wait(0.5)

        # ── Emit gradient arrows one by one ──
        arrows = VGroup()
        arrow_scale = 1.5

        for i in range(5):
            vec = grad_vectors[i] * arrow_scale
            end_point = param_pos + np.array([vec[0], vec[1], 0])

            arrow = Arrow(
                start=param_pos,
                end=end_point,
                color=COLORS[i],
                stroke_width=3,
                buff=0,
                max_tip_length_to_length_ratio=0.15,
            )
            arrows.add(arrow)

            # Highlight the corresponding sidebar entry
            self.play(
                sidebar[i].animate.set_opacity(1.0),
                GrowArrow(arrow),
                run_time=0.7,
            )

            # Special callout for the outlier
            if i == 3:
                outlier_note = Text(
                    "← this one disagrees",
                    font_size=20,
                    color=PURPLE,
                ).next_to(arrow.get_end(), RIGHT, buff=0.15)
                self.play(FadeIn(outlier_note, shift=LEFT * 0.2), run_time=0.4)
                self.wait(0.8)
                self.play(FadeOut(outlier_note), run_time=0.3)

        self.wait(0.5)

        # ── Label: "Each sample votes on which way to move" ──
        vote_text = Text(
            "Each sample votes on which way to move",
            font_size=24,
            color=ACCENT,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(vote_text, shift=UP * 0.2), run_time=0.5)
        self.wait(1.0)

        # ── Merge arrows into resultant ──
        # Compute the mean gradient
        mean_grad = np.mean(grad_vectors, axis=0) * arrow_scale
        resultant_end = param_pos + np.array([mean_grad[0], mean_grad[1], 0])

        resultant = Arrow(
            start=param_pos,
            end=resultant_end,
            color=WHITE,
            stroke_width=5,
            buff=0,
            max_tip_length_to_length_ratio=0.2,
        )

        merge_text = Text(
            "The gradient is just the average",
            font_size=24,
            color=ACCENT,
        ).to_edge(DOWN, buff=0.5)

        self.play(
            *[arrow.animate.set_opacity(0.25) for arrow in arrows],
            ReplacementTransform(vote_text, merge_text),
            GrowArrow(resultant),
            run_time=1.2,
        )
        self.wait(1.0)

        # ── Move the parameter point ──
        new_param_pos = resultant_end
        self.play(
            param_dot.animate.move_to(new_param_pos),
            param_label.animate.next_to(
                Dot(new_param_pos), UR, buff=0.15
            ),
            FadeOut(resultant),
            FadeOut(arrows),
            FadeOut(merge_text),
            run_time=0.8,
        )

        # ── Final beat: zoom on the data ──
        final_text = Text(
            "But individual voices are still in there...",
            font_size=24,
            color=SOFT_WHITE,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(final_text, shift=UP * 0.2), run_time=0.6)
        self.wait(2.0)


class GradientWeathervane(Scene):
    """Remove one data point from a batch and watch the gradient direction change.
    Shows that a single example can measurably redirect the model."""

    def construct(self):
        self.camera.background_color = BG_COLOR

        # Title
        title = Text("The Gradient Weathervane", font_size=36, color=SOFT_WHITE)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title), run_time=0.6)

        # ── Parameter space ──
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=5.5,
            background_line_style={
                "stroke_color": GREY_D,
                "stroke_width": 0.5,
                "stroke_opacity": 0.3,
            },
            axis_config={"stroke_color": GREY_B, "stroke_width": 1},
        ).shift(DOWN * 0.3)

        contours = VGroup()
        for r in [0.8, 1.5, 2.3, 3.0]:
            ellipse = Ellipse(
                width=r * 2.2, height=r * 1.6,
                color=BLUE_E, stroke_width=1, stroke_opacity=0.3,
            ).shift(plane.c2p(-0.5, -0.3))
            contours.add(ellipse)

        self.play(Create(plane), FadeIn(contours), run_time=0.8)

        # Parameter point
        param_pos = plane.c2p(1.5, 1.0)
        param_dot = Dot(param_pos, color=WHITE, radius=0.12)
        self.play(FadeIn(param_dot), run_time=0.3)

        # ── Per-sample gradients (5 data points) ──
        grad_vectors = [
            np.array([-0.8, -0.5]),   # sample A
            np.array([-0.6, -0.7]),   # sample B
            np.array([-0.5, -0.3]),   # sample C
            np.array([-0.3,  1.2]),   # sample D (outlier)
            np.array([-0.7, -0.6]),   # sample E
        ]
        sample_labels = ["A", "B", "C", "D", "E"]
        arrow_scale = 1.5

        # Show all individual arrows
        arrows = VGroup()
        labels = VGroup()
        for i in range(5):
            vec = grad_vectors[i] * arrow_scale
            end_pt = param_pos + np.array([vec[0], vec[1], 0])
            arrow = Arrow(
                start=param_pos, end=end_pt,
                color=COLORS[i], stroke_width=2.5, buff=0,
                max_tip_length_to_length_ratio=0.15,
            )
            label = Text(
                sample_labels[i], font_size=18, color=COLORS[i]
            ).next_to(arrow.get_end(), RIGHT, buff=0.1)
            arrows.add(arrow)
            labels.add(label)

        self.play(
            *[GrowArrow(a) for a in arrows],
            *[FadeIn(l) for l in labels],
            run_time=1.0,
        )
        self.wait(0.5)

        # ── Show full resultant (all 5) ──
        mean_all = np.mean(grad_vectors, axis=0) * arrow_scale
        resultant_all_end = param_pos + np.array([mean_all[0], mean_all[1], 0])
        resultant_all = Arrow(
            start=param_pos, end=resultant_all_end,
            color=WHITE, stroke_width=5, buff=0,
            max_tip_length_to_length_ratio=0.2,
        )
        res_label_all = Text(
            "All 5 samples", font_size=20, color=WHITE
        ).next_to(resultant_all.get_end(), DOWN, buff=0.15)

        self.play(
            *[a.animate.set_opacity(0.2) for a in arrows],
            *[l.animate.set_opacity(0.2) for l in labels],
            GrowArrow(resultant_all),
            FadeIn(res_label_all),
            run_time=0.8,
        )
        self.wait(0.8)

        # ── Remove sample D (the outlier) ──
        remove_text = Text(
            "Remove sample D (the outlier)...",
            font_size=24, color=PURPLE,
        ).to_edge(DOWN, buff=0.5)

        self.play(
            FadeIn(remove_text, shift=UP * 0.2),
            arrows[3].animate.set_opacity(0.0),
            labels[3].animate.set_opacity(0.0),
            run_time=0.6,
        )

        # New resultant without D
        grads_no_d = [grad_vectors[i] for i in [0, 1, 2, 4]]
        mean_no_d = np.mean(grads_no_d, axis=0) * arrow_scale
        resultant_no_d_end = param_pos + np.array([mean_no_d[0], mean_no_d[1], 0])
        resultant_no_d = Arrow(
            start=param_pos, end=resultant_no_d_end,
            color=TEAL, stroke_width=5, buff=0,
            max_tip_length_to_length_ratio=0.2,
        )
        res_label_no_d = Text(
            "Without D", font_size=20, color=TEAL
        ).next_to(resultant_no_d.get_end(), DOWN, buff=0.15)

        self.play(
            GrowArrow(resultant_no_d),
            FadeIn(res_label_no_d),
            run_time=0.8,
        )
        self.wait(0.5)

        # ── Show the angular difference ──
        # Compute the angle between the two resultants
        v1 = mean_all / np.linalg.norm(mean_all)
        v2 = mean_no_d / np.linalg.norm(mean_no_d)
        angle_rad = np.arccos(np.clip(np.dot(v1, v2), -1, 1))
        angle_deg = np.degrees(angle_rad)

        # Draw an arc between them
        angle_start = np.arctan2(mean_all[1], mean_all[0])
        angle_end = np.arctan2(mean_no_d[1], mean_no_d[0])

        # Make sure we go the right way
        if angle_end < angle_start:
            angle_start, angle_end = angle_end, angle_start

        arc = Arc(
            radius=1.2,
            start_angle=angle_start,
            angle=angle_end - angle_start,
            color=ACCENT,
            stroke_width=3,
        ).shift(param_pos)

        angle_label = Text(
            f"{angle_deg:.0f}°",
            font_size=26, color=ACCENT,
        ).next_to(arc, RIGHT, buff=0.2)

        self.play(
            Create(arc),
            FadeIn(angle_label),
            FadeOut(remove_text),
            run_time=0.8,
        )

        rotate_text = Text(
            "One data point rotated the gradient",
            font_size=24, color=ACCENT,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(rotate_text, shift=UP * 0.2), run_time=0.5)
        self.wait(1.5)

        # ── Now swap D for a conformist (E2 ≈ average direction) ──
        self.play(
            FadeOut(resultant_no_d), FadeOut(res_label_no_d),
            FadeOut(arc), FadeOut(angle_label),
            FadeOut(rotate_text),
            run_time=0.5,
        )

        swap_text = Text(
            "Now swap D for a typical sample...",
            font_size=24, color=GREEN,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(swap_text, shift=UP * 0.2), run_time=0.4)

        # Replace D with a conformist gradient
        conformist_grad = np.array([-0.65, -0.55])
        grads_with_conf = [grad_vectors[i] for i in [0, 1, 2, 4]] + [conformist_grad]
        mean_conf = np.mean(grads_with_conf, axis=0) * arrow_scale
        resultant_conf_end = param_pos + np.array([mean_conf[0], mean_conf[1], 0])
        resultant_conf = Arrow(
            start=param_pos, end=resultant_conf_end,
            color=GREEN_C, stroke_width=5, buff=0,
            max_tip_length_to_length_ratio=0.2,
        )
        res_label_conf = Text(
            "With typical sample", font_size=20, color=GREEN_C
        ).next_to(resultant_conf.get_end(), DOWN, buff=0.15)

        self.play(
            GrowArrow(resultant_conf),
            FadeIn(res_label_conf),
            run_time=0.8,
        )

        # Show the (tiny) angle between original and this one
        v3 = mean_conf / np.linalg.norm(mean_conf)
        angle_rad2 = np.arccos(np.clip(np.dot(v1, v3), -1, 1))
        angle_deg2 = np.degrees(angle_rad2)

        barely_text = Text(
            f"Only {angle_deg2:.0f}° change — barely moves",
            font_size=24, color=GREEN,
        ).to_edge(DOWN, buff=0.5)

        self.play(
            ReplacementTransform(swap_text, barely_text),
            run_time=0.5,
        )
        self.wait(1.5)

        # ── Final message ──
        self.play(
            FadeOut(resultant_all), FadeOut(resultant_conf),
            FadeOut(res_label_all), FadeOut(res_label_conf),
            FadeOut(barely_text),
            *[FadeOut(a) for a in arrows],
            *[FadeOut(l) for l in labels],
            run_time=0.6,
        )

        final = VGroup(
            Text(
                "The angular difference is a fingerprint.",
                font_size=28, color=SOFT_WHITE,
            ),
            Text(
                "It measures how much influence one data point has.",
                font_size=28, color=SOFT_WHITE,
            ),
            Text(
                "Next: we'll measure this precisely.",
                font_size=28, color=ACCENT,
            ),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(final, shift=UP * 0.3), run_time=0.8)
        self.wait(2.5)
