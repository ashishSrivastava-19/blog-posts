"""Manim animations for Post 1: What Gradients Actually Tell a Model.

Scenes:
  - UpdateRuleDissected: Build the update equation piece by piece with the ball-on-mountain analogy,
    then show 3 slow, deliberate gradient descent steps with arrows and learning rate labels.
  - GradientForces: Per-sample gradient arrows (forces on the ball) merge into a resultant.
  - GradientFingerprint: Remove one data point, watch the gradient direction shift.

NOTE: Requires a LaTeX installation (e.g. mactex) for MathTex rendering.
"""

from manim import *
import numpy as np


# ──────────────────────────────────────────────
# Color palette
# ──────────────────────────────────────────────
COLORS = [BLUE, GREEN, ORANGE, PURPLE, RED]
BG_COLOR = "#0f0f1a"
ACCENT = "#f0b429"
SOFT_WHITE = "#e0e0e8"
DIM_WHITE = "#888898"


class UpdateRuleDissected(Scene):
    """Build theta_{t+1} = theta_t - eta * nabla L piece by piece.
    Then show 3 slow descent steps, each with a gradient arrow and eta label."""

    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── The full equation (start dimmed) ──
        equation = MathTex(
            r"\theta_{t+1}", "=", r"\theta_t", "-", r"\eta",
            r"\nabla_\theta", r"\mathcal{L}", r"(\theta_t)",
            font_size=60,
        )
        equation.set_color(GREY_D)
        equation.move_to(UP * 1.5)

        self.play(Write(equation), run_time=1.5)
        self.wait(0.5)

        # ── theta_t: "Where you are on the mountain" ──
        label_pos = Text(
            "Where you are on the mountain", font_size=28, color=SOFT_WHITE
        ).next_to(equation, DOWN, buff=1.0)

        self.play(
            equation[2].animate.set_color(BLUE),
            FadeIn(label_pos, shift=UP * 0.3),
            run_time=0.8,
        )
        self.wait(1.2)
        self.play(FadeOut(label_pos), run_time=0.4)

        # ── nabla L: "The slope you feel beneath you" ──
        label_grad = Text(
            "The slope you feel beneath you", font_size=28, color=SOFT_WHITE
        ).next_to(equation, DOWN, buff=1.0)

        self.play(
            equation[5].animate.set_color(RED),
            equation[6].animate.set_color(RED),
            equation[7].animate.set_color(RED),
            FadeIn(label_grad, shift=UP * 0.3),
            run_time=0.8,
        )
        self.wait(1.5)

        label_grad2 = Text(
            "(shaped by the training data)", font_size=22, color=DIM_WHITE
        ).next_to(label_grad, DOWN, buff=0.25)
        self.play(FadeIn(label_grad2, shift=UP * 0.2), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(label_grad), FadeOut(label_grad2), run_time=0.4)

        # ── eta: "How far you roll" ──
        label_lr = Text(
            "How far you roll", font_size=28, color=SOFT_WHITE
        ).next_to(equation, DOWN, buff=1.0)

        self.play(
            equation[4].animate.set_color(GREEN),
            FadeIn(label_lr, shift=UP * 0.3),
            run_time=0.8,
        )
        self.wait(1.2)
        self.play(FadeOut(label_lr), run_time=0.4)

        # ── minus sign: "Downhill, not up" ──
        label_minus = Text(
            "Downhill, not up", font_size=28, color=SOFT_WHITE
        ).next_to(equation, DOWN, buff=1.0)

        self.play(
            equation[3].animate.set_color(ACCENT),
            FadeIn(label_minus, shift=UP * 0.3),
            run_time=0.8,
        )
        self.wait(1.0)
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
            "New position  =  old position  \u2212  step size \u00d7 slope",
            font_size=26,
            color=ACCENT,
        ).next_to(equation, DOWN, buff=1.2)

        self.play(FadeIn(summary, shift=UP * 0.3), run_time=0.8)
        self.wait(2.0)

        # ════════════════════════════════════════════
        # Part 2: Slow, deliberate descent on 1D curve
        # ════════════════════════════════════════════
        self.play(FadeOut(equation), FadeOut(summary), run_time=0.6)

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 5, 1],
            x_length=8,
            y_length=4,
            axis_config={"color": GREY_B, "include_tip": False},
        ).shift(DOWN * 0.3)

        loss_fn = lambda x: 0.4 * x**4 - 1.5 * x**2 + 2.5
        grad_fn = lambda x: 1.6 * x**3 - 3.0 * x

        loss_curve = axes.plot(loss_fn, color=BLUE_C, x_range=[-2.5, 2.5])
        loss_label = axes.get_axis_labels(
            x_label=MathTex(r"\theta", color=SOFT_WHITE),
            y_label=MathTex(r"\mathcal{L}", color=SOFT_WHITE),
        )

        self.play(Create(axes), Create(loss_curve), FadeIn(loss_label), run_time=1.0)

        # Place the ball
        x_val = 2.0
        y_val = loss_fn(x_val)
        ball_glow = Dot(axes.c2p(x_val, y_val), color=ACCENT, radius=0.18).set_opacity(0.25)
        ball = Dot(axes.c2p(x_val, y_val), color=ACCENT, radius=0.1)

        trace = TracedPath(
            ball.get_center, stroke_color=ACCENT, stroke_width=2, stroke_opacity=0.4
        )
        self.add(trace)
        self.play(FadeIn(ball), FadeIn(ball_glow), run_time=0.4)
        self.wait(0.5)

        lr = 0.08

        # ── 3 deliberate descent steps ──
        for step_i in range(3):
            grad = grad_fn(x_val)
            x_new = x_val - lr * grad
            y_new = loss_fn(x_new)

            # 1. Show gradient arrow (pointing uphill = direction of gradient)
            grad_arrow_len = min(abs(grad) * 0.15, 1.5)  # scale for visibility
            grad_dir = np.sign(grad)
            grad_arrow = Arrow(
                start=axes.c2p(x_val, y_val + 0.25),
                end=axes.c2p(x_val + grad_dir * grad_arrow_len, y_val + 0.25),
                color=RED,
                stroke_width=3,
                buff=0,
                max_tip_length_to_length_ratio=0.25,
            )
            grad_label = MathTex(
                r"\nabla \mathcal{L}",
                font_size=24, color=RED,
            ).next_to(grad_arrow, UP, buff=0.1)

            self.play(GrowArrow(grad_arrow), FadeIn(grad_label), run_time=0.6)
            self.wait(0.6)

            # 2. Show the step arrow (opposite direction, scaled by eta)
            step_arrow = Arrow(
                start=axes.c2p(x_val, y_val + 0.25),
                end=axes.c2p(x_new, y_val + 0.25),
                color=GREEN,
                stroke_width=3,
                buff=0,
                max_tip_length_to_length_ratio=0.25,
            )
            eta_label = MathTex(
                r"-\eta \nabla \mathcal{L}",
                font_size=22, color=GREEN,
            ).next_to(step_arrow, DOWN, buff=0.1)

            self.play(
                FadeOut(grad_arrow), FadeOut(grad_label),
                GrowArrow(step_arrow), FadeIn(eta_label),
                run_time=0.6,
            )
            self.wait(0.5)

            # 3. Move the ball
            step_text = Text(
                f"Step {step_i + 1}", font_size=22, color=ACCENT,
            ).to_edge(DOWN, buff=0.5)

            self.play(
                ball.animate.move_to(axes.c2p(x_new, y_new)),
                ball_glow.animate.move_to(axes.c2p(x_new, y_new)),
                FadeIn(step_text),
                run_time=0.8,
            )
            self.wait(0.4)

            # Clean up arrows and labels
            self.play(
                FadeOut(step_arrow), FadeOut(eta_label), FadeOut(step_text),
                run_time=0.4,
            )

            x_val = x_new
            y_val = y_new

        # ── Settled label ──
        settled = Text(
            "The ball rolls downhill, one step at a time",
            font_size=24, color=ACCENT,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(settled, shift=UP * 0.2), run_time=0.5)
        self.wait(2.5)


class GradientForces(Scene):
    """Five data points each exert a force (gradient arrow) on the ball.
    Forces merge into a resultant — showing the gradient as a tug of war.
    All explanatory text appears at the bottom."""

    def construct(self):
        self.camera.background_color = BG_COLOR

        # Title
        title = Text("Forces on the Ball", font_size=36, color=SOFT_WHITE)
        subtitle = Text(
            "Each data point pulls in its own direction",
            font_size=20, color=DIM_WHITE,
        )
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.2)
        header.to_edge(UP, buff=0.3)
        self.play(FadeIn(header), run_time=0.6)

        # ── Parameter space ──
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=5,
            background_line_style={
                "stroke_color": GREY_D,
                "stroke_width": 0.5,
                "stroke_opacity": 0.2,
            },
            axis_config={"stroke_color": GREY_B, "stroke_width": 1},
        ).shift(DOWN * 0.4)

        contours = VGroup()
        for r in [0.8, 1.5, 2.3, 3.0]:
            ellipse = Ellipse(
                width=r * 2.2, height=r * 1.6,
                color=BLUE_E, stroke_width=1, stroke_opacity=0.2,
            ).shift(plane.c2p(-0.5, -0.3))
            contours.add(ellipse)

        self.play(Create(plane), FadeIn(contours), run_time=0.8)

        # The ball
        param_pos = plane.c2p(1.5, 1.0)
        ball_glow = Dot(param_pos, color=ACCENT, radius=0.18).set_opacity(0.25)
        ball = Dot(param_pos, color=ACCENT, radius=0.12)
        ball_label = MathTex(r"\theta_t", font_size=26, color=ACCENT).next_to(
            ball, UR, buff=0.15
        )
        self.play(FadeIn(ball), FadeIn(ball_glow), FadeIn(ball_label), run_time=0.4)

        # ── Data points in sidebar ──
        data_labels = [
            "cat photo",
            "dog photo",
            "blurry cat",
            "rare bird",
            "dog again",
        ]
        grad_vectors = [
            np.array([-0.8, -0.5]),
            np.array([-0.6, -0.7]),
            np.array([-0.5, -0.3]),
            np.array([-0.3,  1.2]),   # outlier
            np.array([-0.7, -0.6]),
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
        self.wait(0.3)

        # ── Emit force arrows one by one ──
        arrows = VGroup()
        arrow_scale = 1.5

        for i in range(5):
            vec = grad_vectors[i] * arrow_scale
            end_point = param_pos + np.array([vec[0], vec[1], 0])

            arrow = Arrow(
                start=param_pos, end=end_point,
                color=COLORS[i], stroke_width=3, buff=0,
                max_tip_length_to_length_ratio=0.15,
            )
            arrows.add(arrow)

            self.play(
                sidebar[i].animate.set_opacity(1.0),
                GrowArrow(arrow),
                run_time=0.6,
            )

            # Callout for the outlier — this is a label on the arrow, stays near it
            if i == 3:
                outlier_note = Text(
                    "\u2190 pulls a completely different way",
                    font_size=18, color=PURPLE,
                ).next_to(arrow.get_end(), RIGHT, buff=0.15)
                self.play(FadeIn(outlier_note, shift=LEFT * 0.2), run_time=0.4)
                self.wait(0.8)
                self.play(FadeOut(outlier_note), run_time=0.3)

        self.wait(0.3)

        # ── Explanatory text at bottom ──
        tug_text = Text(
            "Five data points, five different forces",
            font_size=22, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(tug_text, shift=UP * 0.2), run_time=0.5)
        self.wait(0.8)

        # ── Merge into resultant ──
        mean_grad = np.mean(grad_vectors, axis=0) * arrow_scale
        resultant_end = param_pos + np.array([mean_grad[0], mean_grad[1], 0])

        resultant = Arrow(
            start=param_pos, end=resultant_end,
            color=WHITE, stroke_width=5, buff=0,
            max_tip_length_to_length_ratio=0.2,
        )

        merge_text = Text(
            "The gradient you feel = the average of all forces",
            font_size=22, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            *[arrow.animate.set_opacity(0.2) for arrow in arrows],
            ReplacementTransform(tug_text, merge_text),
            GrowArrow(resultant),
            run_time=1.2,
        )
        self.wait(1.0)

        # ── Roll the ball ──
        new_param_pos = resultant_end
        self.play(
            ball.animate.move_to(new_param_pos),
            ball_glow.animate.move_to(new_param_pos),
            ball_label.animate.next_to(Dot(new_param_pos), UR, buff=0.15),
            FadeOut(resultant), FadeOut(arrows), FadeOut(merge_text),
            run_time=0.8,
        )

        # ── Final explanatory text at bottom ──
        final_text = Text(
            "But every individual pull is still in there...",
            font_size=22, color=SOFT_WHITE,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(final_text, shift=UP * 0.2), run_time=0.6)
        self.wait(2.0)


class GradientFingerprint(Scene):
    """Remove one data point from a batch and watch the gradient direction shift.
    The angular difference is a 'fingerprint' of that data point's influence.
    All explanatory text appears at the bottom."""

    def construct(self):
        self.camera.background_color = BG_COLOR

        # Title
        title = Text("The Gradient Fingerprint", font_size=36, color=SOFT_WHITE)
        subtitle = Text(
            "How much does one data point change the slope?",
            font_size=20, color=DIM_WHITE,
        )
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.2)
        header.to_edge(UP, buff=0.3)
        self.play(FadeIn(header), run_time=0.6)

        # ── Parameter space ──
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=5,
            background_line_style={
                "stroke_color": GREY_D,
                "stroke_width": 0.5,
                "stroke_opacity": 0.2,
            },
            axis_config={"stroke_color": GREY_B, "stroke_width": 1},
        ).shift(DOWN * 0.4)

        contours = VGroup()
        for r in [0.8, 1.5, 2.3, 3.0]:
            ellipse = Ellipse(
                width=r * 2.2, height=r * 1.6,
                color=BLUE_E, stroke_width=1, stroke_opacity=0.2,
            ).shift(plane.c2p(-0.5, -0.3))
            contours.add(ellipse)

        self.play(Create(plane), FadeIn(contours), run_time=0.8)

        # Ball
        param_pos = plane.c2p(1.5, 1.0)
        ball_glow = Dot(param_pos, color=ACCENT, radius=0.18).set_opacity(0.25)
        ball = Dot(param_pos, color=ACCENT, radius=0.12)
        self.play(FadeIn(ball), FadeIn(ball_glow), run_time=0.3)

        # ── Per-sample forces ──
        grad_vectors = [
            np.array([-0.8, -0.5]),
            np.array([-0.6, -0.7]),
            np.array([-0.5, -0.3]),
            np.array([-0.3,  1.2]),   # outlier
            np.array([-0.7, -0.6]),
        ]
        sample_labels = ["A", "B", "C", "D", "E"]
        arrow_scale = 1.5

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

        # ── Resultant with all 5 ──
        mean_all = np.mean(grad_vectors, axis=0) * arrow_scale
        resultant_all_end = param_pos + np.array([mean_all[0], mean_all[1], 0])
        resultant_all = Arrow(
            start=param_pos, end=resultant_all_end,
            color=WHITE, stroke_width=5, buff=0,
            max_tip_length_to_length_ratio=0.2,
        )
        res_label_all = Text(
            "All 5 forces", font_size=20, color=WHITE
        ).next_to(resultant_all.get_end(), DOWN, buff=0.15)

        self.play(
            *[a.animate.set_opacity(0.15) for a in arrows],
            *[l.animate.set_opacity(0.15) for l in labels],
            GrowArrow(resultant_all),
            FadeIn(res_label_all),
            run_time=0.8,
        )
        self.wait(0.8)

        # ── Remove sample D ──
        remove_text = Text(
            "Remove sample D (the outlier)...",
            font_size=22, color=PURPLE,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            FadeIn(remove_text, shift=UP * 0.2),
            arrows[3].animate.set_opacity(0.0),
            labels[3].animate.set_opacity(0.0),
            run_time=0.6,
        )

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

        # ── Angular difference ──
        v1 = mean_all / np.linalg.norm(mean_all)
        v2 = mean_no_d / np.linalg.norm(mean_no_d)
        angle_rad = np.arccos(np.clip(np.dot(v1, v2), -1, 1))
        angle_deg = np.degrees(angle_rad)

        angle_start = np.arctan2(mean_all[1], mean_all[0])
        angle_end = np.arctan2(mean_no_d[1], mean_no_d[0])
        if angle_end < angle_start:
            angle_start, angle_end = angle_end, angle_start

        arc = Arc(
            radius=1.2,
            start_angle=angle_start,
            angle=angle_end - angle_start,
            color=ACCENT, stroke_width=3,
        ).shift(param_pos)

        # Angle label — this is a measurement label, stays near the arc
        angle_label = Text(
            f"{angle_deg:.0f}\u00b0", font_size=28, color=ACCENT,
        ).next_to(arc, RIGHT, buff=0.2)

        # Explanatory text at bottom
        fingerprint_text = Text(
            "One data point shifted the slope this much",
            font_size=22, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            Create(arc), FadeIn(angle_label),
            ReplacementTransform(remove_text, fingerprint_text),
            run_time=0.8,
        )
        self.wait(1.5)

        # ── Swap D for a typical sample ──
        self.play(
            FadeOut(resultant_no_d), FadeOut(res_label_no_d),
            FadeOut(arc), FadeOut(angle_label),
            FadeOut(fingerprint_text),
            run_time=0.5,
        )

        swap_text = Text(
            "Now replace D with a typical sample...",
            font_size=22, color=GREEN,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(swap_text, shift=UP * 0.2), run_time=0.4)

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
            GrowArrow(resultant_conf), FadeIn(res_label_conf),
            run_time=0.8,
        )

        v3 = mean_conf / np.linalg.norm(mean_conf)
        angle_rad2 = np.arccos(np.clip(np.dot(v1, v3), -1, 1))
        angle_deg2 = np.degrees(angle_rad2)

        barely_text = Text(
            f"Only {angle_deg2:.0f}\u00b0 change \u2014 barely a nudge",
            font_size=22, color=GREEN,
        ).to_edge(DOWN, buff=0.4)

        self.play(ReplacementTransform(swap_text, barely_text), run_time=0.5)
        self.wait(1.5)

        # ── Final message — at bottom, not centre ──
        self.play(
            FadeOut(resultant_all), FadeOut(resultant_conf),
            FadeOut(res_label_all), FadeOut(res_label_conf),
            FadeOut(barely_text),
            *[FadeOut(a) for a in arrows],
            *[FadeOut(l) for l in labels],
            run_time=0.6,
        )

        final_lines = VGroup(
            Text("That angular shift is a fingerprint.", font_size=26, color=SOFT_WHITE),
            Text("It measures one data point's influence on the ball.", font_size=26, color=SOFT_WHITE),
            Text("Next: we measure this precisely.", font_size=26, color=ACCENT),
        ).arrange(DOWN, buff=0.3)
        final_lines.to_edge(DOWN, buff=0.6)

        self.play(FadeIn(final_lines, shift=UP * 0.3), run_time=0.8)
        self.wait(2.5)
