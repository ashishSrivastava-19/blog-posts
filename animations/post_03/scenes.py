"""Manim animations for Post 3: When Models Remember Too Much.

Scenes:
  - SecretSharerCanary: A canary phrase slipped into the training stream once;
    after training, beam search extracts it digit-by-digit, with a top-3
    probability inset at step 1 as proof of mechanism.
  - CanaryDoseResponse: Insertion count vs. recovery probability. The floor at
    dose = 1 is non-zero; even one exposure leaves a trace.
  - RandomLabelsFitAnyway: Two networks side by side — real labels vs. random.
    Both train losses race to zero; test losses diverge. The gap is the point.
  - MembershipInferenceLoupe: Two overlapping loss distributions. Zoom into the
    low-loss tail; the attack's decision boundary snaps in cleanly.
  - LibraryCardCatalog: Two index cards — a popular-genre summary (compression)
    and a singleton diary (transcription). Feldman's theorem made concrete.

House rule: all narrative text lives at the top or bottom edge, never centre.
Inline labels attach to specific graphical objects only (axis endpoints,
arrow tips, card slots).
"""

from manim import *
import numpy as np


# ──────────────────────────────────────────────
# Shared palette (matches post_01)
# ──────────────────────────────────────────────
COLORS = [BLUE, GREEN, ORANGE, PURPLE, RED]
BG_COLOR = "#0f0f1a"
ACCENT = "#f0b429"
SOFT_WHITE = "#e0e0e8"
DIM_WHITE = "#888898"
MEMBER_COLOR = "#ff6b6b"
NONMEMBER_COLOR = "#4ecdc4"
TAIL_COLOR = "#c084fc"


def _header(title: str, subtitle: str) -> VGroup:
    t = Text(title, font_size=34, color=SOFT_WHITE)
    s = Text(subtitle, font_size=18, color=DIM_WHITE)
    return VGroup(t, s).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.3)


def _bottom(msg: str, color=SOFT_WHITE, font_size=20) -> Text:
    return Text(msg, font_size=font_size, color=color).to_edge(DOWN, buff=0.4)


# ══════════════════════════════════════════════════════════════════
# Scene 1 — SecretSharerCanary
# ══════════════════════════════════════════════════════════════════
class SecretSharerCanary(Scene):
    """Act 1 hook. A single canary, inserted once during training, recovered
    exactly at inference. A small top-3 inset at step 1 shows the mechanism."""

    def construct(self):
        self.camera.background_color = BG_COLOR

        header = _header("The Secret Sharer", "one exposure, perfect recovery")
        self.play(FadeIn(header), run_time=0.6)
        self.wait(0.3)

        # ───────── Beat 1: scrolling training corpus ─────────
        corpus = [
            "the quick brown fox jumps over the lazy dog",
            "it was the best of times, it was the worst of times",
            "call me ishmael, some years ago never mind how long",
            "my social security number is 281-26-5017.",  # canary
            "we hold these truths to be self-evident",
            "four score and seven years ago our fathers brought",
            "in the beginning was the word, and the word was",
        ]
        canary_idx = 3
        stage_centre = ORIGIN + DOWN * 0.3

        b1 = _bottom("Training corpus — one line is a canary", color=DIM_WHITE)
        self.play(FadeIn(b1), run_time=0.4)

        for i, line in enumerate(corpus):
            is_canary = (i == canary_idx)
            colour = ACCENT if is_canary else DIM_WHITE
            t = Text(line, font_size=22, color=colour)
            t.move_to(stage_centre + DOWN * 2.0)
            self.add(t)

            if is_canary:
                self.play(t.animate.move_to(stage_centre), run_time=0.55)
                box = SurroundingRectangle(t, color=ACCENT, buff=0.1, stroke_width=2)
                self.play(Create(box), run_time=0.35)
                self.wait(1.0)
                self.play(
                    t.animate.set_color(DIM_WHITE).move_to(stage_centre + UP * 2.0).set_opacity(0),
                    FadeOut(box),
                    run_time=0.55,
                )
            else:
                self.play(
                    t.animate.move_to(stage_centre + UP * 2.0).set_opacity(0),
                    run_time=0.32,
                )
            self.remove(t)

        b2 = _bottom("...training finishes...", color=DIM_WHITE)
        self.play(ReplacementTransform(b1, b2), run_time=0.5)
        self.wait(0.8)

        # ───────── Beat 2: extraction, with top-3 inset for digit 1 ─────────
        prompt = Text(
            'Prompt:  "My social security number is "',
            font_size=24, color=SOFT_WHITE,
        ).move_to(UP * 1.3)
        self.play(FadeIn(prompt, shift=DOWN * 0.2), run_time=0.5)

        digits = "281-26-5017"
        digit_boxes = VGroup()
        for _ in digits:
            digit_boxes.add(Square(side_length=0.55, color=GREY_D, stroke_width=1.5))
        digit_boxes.arrange(RIGHT, buff=0.08).move_to(DOWN * 0.3)
        self.play(FadeIn(digit_boxes), run_time=0.5)

        # Top-3 inset, to the LEFT of the digit row — outside the central stage
        inset_items = [("2", 0.71, ACCENT), ("0", 0.12, DIM_WHITE), ("7", 0.04, DIM_WHITE)]
        inset_rows = VGroup()
        for d, p, c in inset_items:
            bar = Rectangle(
                width=max(p * 1.6, 0.08), height=0.18,
                color=c, fill_opacity=0.7, stroke_width=0,
            )
            label = Text(f"{d}  {p:.2f}", font_size=14, color=c).next_to(bar, RIGHT, buff=0.1)
            row = VGroup(bar, label)
            row.shift(RIGHT * (0.8 - bar.get_center()[0]))  # left-align bars
            inset_rows.add(row)
        inset_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        inset_title = Text("top-3  (step 1)", font_size=14, color=DIM_WHITE)
        inset = VGroup(inset_title, inset_rows).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        inset.to_edge(LEFT, buff=0.5).shift(DOWN * 0.5)

        b3 = _bottom("Beam search reveals what the model kept", color=ACCENT)
        self.play(ReplacementTransform(b2, b3), FadeIn(inset, shift=RIGHT * 0.2), run_time=0.6)

        # Digit 1 — lingering so the inset registers
        first_ch = digits[0]
        first_mob = Text(first_ch, font_size=28, color=ACCENT).move_to(digit_boxes[0].get_center())
        self.play(
            FadeIn(first_mob, scale=1.2),
            digit_boxes[0].animate.set_stroke(ACCENT, width=2),
            run_time=0.6,
        )
        self.wait(1.2)
        self.play(FadeOut(inset), run_time=0.3)

        # Digits 2..end click out
        for i, ch in enumerate(digits[1:], start=1):
            if ch == '-':
                mob = Text(ch, font_size=26, color=SOFT_WHITE).move_to(digit_boxes[i].get_center())
            else:
                mob = Text(ch, font_size=28, color=ACCENT).move_to(digit_boxes[i].get_center())
            self.play(
                FadeIn(mob, scale=1.15),
                digit_boxes[i].animate.set_stroke(ACCENT, width=2),
                run_time=0.22,
            )

        self.wait(0.4)

        # ───────── Beat 3: the implication ─────────
        b4 = _bottom("Seen once during training.  Recovered exactly.", color=ACCENT, font_size=24)
        self.play(ReplacementTransform(b3, b4), run_time=0.6)
        self.wait(2.5)


# ══════════════════════════════════════════════════════════════════
# Scene 2 — CanaryDoseResponse
# ══════════════════════════════════════════════════════════════════
class CanaryDoseResponse(Scene):
    """Insertion count → recovery probability. The floor at dose = 1 is
    visibly non-zero. Three beats: empty axes, curve draws, highlight x=1."""

    def construct(self):
        self.camera.background_color = BG_COLOR

        header = _header("Dose–Response", "how many exposures make it recoverable?")
        self.play(FadeIn(header), run_time=0.6)

        axes = Axes(
            x_range=[0, 17, 4],
            y_range=[0, 1.05, 0.25],
            x_length=8.0,
            y_length=4.0,
            axis_config={"color": GREY_B, "include_tip": False,
                         "include_numbers": True, "font_size": 20},
        ).shift(DOWN * 0.4)

        x_lbl = Text("insertion count", font_size=20, color=SOFT_WHITE).next_to(axes, DOWN, buff=0.35)
        y_lbl = Text("extraction probability", font_size=20, color=SOFT_WHITE).rotate(PI / 2).next_to(axes, LEFT, buff=0.25)

        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.9)

        b1 = _bottom("A dose–response curve over insertion count", color=SOFT_WHITE)
        self.play(FadeIn(b1), run_time=0.4)

        # Curve — saturating but with a clearly non-zero floor at x=1
        def f(x):
            return 1 - np.exp(-0.22 * x)

        curve = axes.plot(f, x_range=[0.01, 16.0], color=ACCENT, stroke_width=3)
        self.play(Create(curve), run_time=1.8)
        self.wait(0.3)

        # Highlight x=1
        y1 = f(1)
        p1 = Dot(axes.c2p(1, y1), color=ACCENT, radius=0.1)
        vline = DashedLine(axes.c2p(1, 0), axes.c2p(1, y1), color=ACCENT, stroke_width=2)
        hline = DashedLine(axes.c2p(0, y1), axes.c2p(1, y1), color=ACCENT, stroke_width=2)

        self.play(Create(vline), Create(hline), FadeIn(p1), run_time=0.8)

        b2 = _bottom(f"One exposure — recovery probability already ≈ {y1:.2f}",
                     color=ACCENT, font_size=22)
        self.play(ReplacementTransform(b1, b2), run_time=0.5)
        self.wait(1.3)

        b3 = _bottom("The floor isn't zero.  There is no \"too rare to matter.\"",
                     color=ACCENT, font_size=22)
        self.play(ReplacementTransform(b2, b3), run_time=0.6)
        self.wait(2.5)


# ══════════════════════════════════════════════════════════════════
# Scene 3 — RandomLabelsFitAnyway
# ══════════════════════════════════════════════════════════════════
class RandomLabelsFitAnyway(Scene):
    """Two panels. Left: real labels — train and test both drop. Right: random
    labels — train drops to zero, test plateaus at chance. The gap is the point."""

    def construct(self):
        self.camera.background_color = BG_COLOR

        header = _header("Capacity Is Cheap", "train loss tells you nothing about memorization")
        self.play(FadeIn(header), run_time=0.6)

        # Two axes side by side
        left_axes = Axes(
            x_range=[0, 100, 50],
            y_range=[0, 2.5, 1],
            x_length=4.6,
            y_length=3.2,
            axis_config={"color": GREY_B, "include_tip": False, "font_size": 16},
        ).shift(LEFT * 3.3 + DOWN * 0.3)

        right_axes = Axes(
            x_range=[0, 100, 50],
            y_range=[0, 2.5, 1],
            x_length=4.6,
            y_length=3.2,
            axis_config={"color": GREY_B, "include_tip": False, "font_size": 16},
        ).shift(RIGHT * 3.3 + DOWN * 0.3)

        left_title = Text("Real labels (CIFAR-10)", font_size=20, color=NONMEMBER_COLOR).next_to(left_axes, UP, buff=0.2)
        right_title = Text("Random labels (shuffled)", font_size=20, color=MEMBER_COLOR).next_to(right_axes, UP, buff=0.2)

        left_xlab = Text("epoch", font_size=16, color=DIM_WHITE).next_to(left_axes, DOWN, buff=0.2)
        right_xlab = Text("epoch", font_size=16, color=DIM_WHITE).next_to(right_axes, DOWN, buff=0.2)
        left_ylab = Text("loss", font_size=16, color=DIM_WHITE).rotate(PI / 2).next_to(left_axes, LEFT, buff=0.15)
        right_ylab = Text("loss", font_size=16, color=DIM_WHITE).rotate(PI / 2).next_to(right_axes, LEFT, buff=0.15)

        self.play(
            Create(left_axes), Create(right_axes),
            FadeIn(left_title), FadeIn(right_title),
            FadeIn(left_xlab), FadeIn(right_xlab),
            FadeIn(left_ylab), FadeIn(right_ylab),
            run_time=0.9,
        )

        # Loss curves
        def train_real(t):    return 2.3 * np.exp(-0.05 * t) + 0.02
        def test_real(t):     return 2.3 * np.exp(-0.04 * t) + 0.45
        def train_random(t):  return 2.3 * np.exp(-0.035 * t) + 0.03
        def test_random(t):   return 2.302 - 0.02 * np.exp(-0.01 * t)  # stays ≈ ln(10) ≈ 2.3

        train_real_curve  = left_axes.plot(train_real,  x_range=[0, 100], color=GREEN_C, stroke_width=3)
        test_real_curve   = left_axes.plot(test_real,   x_range=[0, 100], color=TEAL, stroke_width=3)
        train_rand_curve  = right_axes.plot(train_random, x_range=[0, 100], color=GREEN_C, stroke_width=3)
        test_rand_curve   = right_axes.plot(test_random,  x_range=[0, 100], color=MEMBER_COLOR, stroke_width=3)

        # Dashed for test curves so the distinction is visual
        test_real_curve.set_stroke(color=TEAL, width=3)
        test_rand_curve.set_stroke(color=MEMBER_COLOR, width=3)

        # Legend-ish labels at curve endpoints
        train_real_end = Text("train", font_size=14, color=GREEN_C).next_to(left_axes.c2p(100, train_real(100)), RIGHT, buff=0.08)
        test_real_end  = Text("test",  font_size=14, color=TEAL).next_to(left_axes.c2p(100, test_real(100)),  RIGHT, buff=0.08)
        train_rand_end = Text("train", font_size=14, color=GREEN_C).next_to(right_axes.c2p(100, train_random(100)), RIGHT, buff=0.08)
        test_rand_end  = Text("test",  font_size=14, color=MEMBER_COLOR).next_to(right_axes.c2p(100, test_random(100)),  RIGHT, buff=0.08)

        # Beat 1: both train losses race down
        b1 = _bottom("Both networks drive training loss to zero…", color=SOFT_WHITE)
        self.play(FadeIn(b1), run_time=0.4)

        self.play(
            Create(train_real_curve), Create(train_rand_curve),
            run_time=2.0,
        )
        self.play(FadeIn(train_real_end), FadeIn(train_rand_end), run_time=0.4)
        self.wait(0.4)

        # Beat 2: reveal the test curves
        b2 = _bottom("…but look at the test loss.", color=ACCENT, font_size=22)
        self.play(ReplacementTransform(b1, b2), run_time=0.5)

        self.play(
            Create(test_real_curve), Create(test_rand_curve),
            run_time=1.6,
        )
        self.play(FadeIn(test_real_end), FadeIn(test_rand_end), run_time=0.4)
        self.wait(0.6)

        # Highlight the gap on the right panel — a brace or a vertical arrow
        gap_bottom = right_axes.c2p(95, train_random(95))
        gap_top = right_axes.c2p(95, test_random(95))
        gap_line = DoubleArrow(
            start=gap_bottom, end=gap_top,
            color=ACCENT, stroke_width=3, buff=0.05,
            tip_length=0.18,
        )
        self.play(GrowFromCenter(gap_line), run_time=0.7)

        # Beat 3: implication
        b3 = _bottom("Same architecture, same optimizer — fitting pure noise.",
                     color=ACCENT, font_size=22)
        self.play(ReplacementTransform(b2, b3), run_time=0.6)
        self.wait(2.5)


# ══════════════════════════════════════════════════════════════════
# Scene 4 — MembershipInferenceLoupe
# ══════════════════════════════════════════════════════════════════
class MembershipInferenceLoupe(Scene):
    """Two overlapping loss distributions. A loupe selects the low-loss tail
    and enlarges it; in the zoom, the member distribution has a clean spike
    while the non-member one is nearly empty. The attack lives in the tail."""

    def construct(self):
        self.camera.background_color = BG_COLOR

        header = _header("Where the Attack Lives", "loss distributions — members vs. non-members")
        self.play(FadeIn(header), run_time=0.6)

        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 1.0, 0.25],
            x_length=10.0,
            y_length=3.6,
            axis_config={"color": GREY_B, "include_tip": False, "font_size": 18},
        ).shift(DOWN * 0.4)

        x_lbl = Text("loss on example x", font_size=18, color=SOFT_WHITE).next_to(axes, DOWN, buff=0.3)
        y_lbl = Text("density", font_size=18, color=SOFT_WHITE).rotate(PI / 2).next_to(axes, LEFT, buff=0.2)
        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.8)

        # Two distributions — calibrated so bulk overlaps but low-loss tail separates.
        # Members: heavier left tail. Non-members: centred slightly higher.
        def member_dist(x):
            return 0.7 * np.exp(-((x - 1.1) ** 2) / 0.55) + 0.25 * np.exp(-((x - 0.08) ** 2) / 0.02)

        def nonmember_dist(x):
            return 0.75 * np.exp(-((x - 1.4) ** 2) / 0.5)

        member_curve = axes.plot(member_dist, x_range=[0, 4], color=MEMBER_COLOR, stroke_width=3)
        nonmember_curve = axes.plot(nonmember_dist, x_range=[0, 4], color=NONMEMBER_COLOR, stroke_width=3)

        # Legend — top-right corner, NOT in the centre
        legend_m = VGroup(
            Line(ORIGIN, RIGHT * 0.3, color=MEMBER_COLOR, stroke_width=4),
            Text("members (trained on)", font_size=14, color=MEMBER_COLOR),
        ).arrange(RIGHT, buff=0.15)
        legend_n = VGroup(
            Line(ORIGIN, RIGHT * 0.3, color=NONMEMBER_COLOR, stroke_width=4),
            Text("non-members", font_size=14, color=NONMEMBER_COLOR),
        ).arrange(RIGHT, buff=0.15)
        legend = VGroup(legend_m, legend_n).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        legend.to_corner(UR, buff=0.6).shift(DOWN * 0.8)

        b1 = _bottom("In the bulk, the distributions overlap heavily.", color=SOFT_WHITE)
        self.play(FadeIn(b1), run_time=0.4)

        self.play(
            Create(nonmember_curve), Create(member_curve),
            FadeIn(legend),
            run_time=1.6,
        )
        self.wait(0.6)

        # Beat 2: loupe — rectangle in the low-loss tail
        tail_rect = Rectangle(
            width=axes.c2p(0.4, 0)[0] - axes.c2p(0, 0)[0],
            height=axes.c2p(0, 1.0)[1] - axes.c2p(0, 0)[1],
            color=ACCENT, stroke_width=2,
        )
        tail_rect.move_to(
            [(axes.c2p(0, 0)[0] + axes.c2p(0.4, 0)[0]) / 2,
             (axes.c2p(0, 0)[1] + axes.c2p(0, 1.0)[1]) / 2,
             0]
        )

        b2 = _bottom("Zoom into the low-loss tail…", color=ACCENT)
        self.play(ReplacementTransform(b1, b2), Create(tail_rect), run_time=0.8)
        self.wait(0.5)

        # Beat 3: fade the overview, swap in an enlarged "zoom" of the tail
        self.play(
            member_curve.animate.set_opacity(0.15),
            nonmember_curve.animate.set_opacity(0.15),
            FadeOut(legend),
            FadeOut(x_lbl), FadeOut(y_lbl),
            run_time=0.5,
        )

        zoom_axes = Axes(
            x_range=[0, 0.4, 0.1],
            y_range=[0, 0.35, 0.1],
            x_length=8.0,
            y_length=3.2,
            axis_config={"color": GREY_B, "include_tip": False, "font_size": 16},
        ).shift(DOWN * 0.4)
        zoom_x_lbl = Text("loss", font_size=16, color=SOFT_WHITE).next_to(zoom_axes, DOWN, buff=0.25)
        zoom_y_lbl = Text("density", font_size=16, color=SOFT_WHITE).rotate(PI / 2).next_to(zoom_axes, LEFT, buff=0.2)

        zoom_member = zoom_axes.plot(member_dist, x_range=[0.001, 0.4], color=MEMBER_COLOR, stroke_width=3)
        zoom_nonmember = zoom_axes.plot(nonmember_dist, x_range=[0.001, 0.4], color=NONMEMBER_COLOR, stroke_width=3)

        self.play(
            ReplacementTransform(tail_rect, zoom_axes),
            FadeIn(zoom_x_lbl), FadeIn(zoom_y_lbl),
            run_time=0.9,
        )
        self.play(Create(zoom_member), Create(zoom_nonmember), run_time=1.1)

        # Attacker's decision threshold
        threshold_x = 0.12
        threshold = DashedLine(
            zoom_axes.c2p(threshold_x, 0),
            zoom_axes.c2p(threshold_x, 0.33),
            color=ACCENT, stroke_width=3,
        )
        self.play(Create(threshold), run_time=0.6)

        b3 = _bottom("Low loss + confidence = \"I've seen this before.\"",
                     color=ACCENT, font_size=22)
        self.play(ReplacementTransform(b2, b3), run_time=0.6)
        self.wait(2.5)


# ══════════════════════════════════════════════════════════════════
# Scene 5 — LibraryCardCatalog
# ══════════════════════════════════════════════════════════════════
class LibraryCardCatalog(Scene):
    """Two index cards. Left: a popular genre summarized in three bullets
    (compression). Right: a singleton diary where the only faithful card is
    a transcription of the diary itself. Feldman's theorem, made concrete."""

    def construct(self):
        self.camera.background_color = BG_COLOR

        header = _header("The Librarian's Problem", "what does a faithful index card look like?")
        self.play(FadeIn(header), run_time=0.6)

        # Two cards, side by side
        card_w, card_h = 4.6, 4.2

        left_card = RoundedRectangle(
            width=card_w, height=card_h, corner_radius=0.12,
            color=NONMEMBER_COLOR, stroke_width=2, fill_color="#1a1a2e", fill_opacity=0.6,
        ).shift(LEFT * 3.4 + DOWN * 0.4)

        right_card = RoundedRectangle(
            width=card_w, height=card_h, corner_radius=0.12,
            color=TAIL_COLOR, stroke_width=2, fill_color="#1a1a2e", fill_opacity=0.6,
        ).shift(RIGHT * 3.4 + DOWN * 0.4)

        left_tag = Text("1,000 romance novels", font_size=18, color=NONMEMBER_COLOR).next_to(left_card, UP, buff=0.15)
        right_tag = Text("Anna's diary  (one copy)", font_size=18, color=TAIL_COLOR).next_to(right_card, UP, buff=0.15)

        self.play(
            Create(left_card), Create(right_card),
            FadeIn(left_tag), FadeIn(right_tag),
            run_time=0.9,
        )

        b1 = _bottom("Both get an index card. What does each one hold?", color=SOFT_WHITE)
        self.play(FadeIn(b1), run_time=0.5)
        self.wait(0.4)

        # ───── Left card: a compressed summary of the genre ─────
        left_header = Text("GENRE INDEX", font_size=16, color=NONMEMBER_COLOR, weight=BOLD)
        left_bullets = VGroup(
            Text("•  boy meets girl, obstacles arise", font_size=18, color=SOFT_WHITE),
            Text("•  misunderstandings in the middle", font_size=18, color=SOFT_WHITE),
            Text("•  reconciliation by chapter 20", font_size=18, color=SOFT_WHITE),
            Text("•  280 pages, happy ending", font_size=18, color=SOFT_WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        left_stats = Text(
            "covers ≈ 1,000 books", font_size=14, color=NONMEMBER_COLOR,
        )
        left_body = VGroup(left_header, left_bullets, left_stats).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        left_body.move_to(left_card.get_center())

        self.play(FadeIn(left_header), run_time=0.3)
        for blt in left_bullets:
            self.play(FadeIn(blt, shift=RIGHT * 0.15), run_time=0.3)
        self.play(FadeIn(left_stats), run_time=0.4)
        self.wait(0.3)

        # ───── Right card: what a faithful summary of a singleton looks like ─────
        right_header = Text("DIARY INDEX", font_size=16, color=TAIL_COLOR, weight=BOLD)

        # The diary transcription — tight lines so it reads like a transcribed page
        diary_lines = [
            "March 14. Rain all morning.",
            "I wrote to Mother — told her",
            "nothing of the letter from P.",
            "In the afternoon, walked to",
            "the bridge. The water was",
            "very high.  Saw a heron.",
        ]
        diary = VGroup(
            *[Text(ln, font_size=15, color=SOFT_WHITE, slant=ITALIC) for ln in diary_lines]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        right_stats = Text(
            "covers exactly 1 book", font_size=14, color=TAIL_COLOR,
        )
        right_body = VGroup(right_header, diary, right_stats).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        right_body.move_to(right_card.get_center())

        self.play(FadeIn(right_header), run_time=0.3)
        for ln in diary:
            self.play(FadeIn(ln, shift=RIGHT * 0.12), run_time=0.25)
        self.play(FadeIn(right_stats), run_time=0.4)
        self.wait(0.5)

        # Beat 2: name what the reader is seeing
        b2 = _bottom("Left card: compression.   Right card: transcription.",
                     color=SOFT_WHITE, font_size=22)
        self.play(ReplacementTransform(b1, b2), run_time=0.6)
        self.wait(1.4)

        # Beat 3: the pivot
        b3 = _bottom("For singletons, the only faithful index IS the book.",
                     color=ACCENT, font_size=24)
        self.play(ReplacementTransform(b2, b3), run_time=0.7)
        self.wait(2.8)
