"""Manim animations for Post 4: Differential Privacy: The Math of Plausible Deniability.

Scenes:
  - SweenyJoinAttack: anonymized hospital records on the left, public voter roll
    on the right, joined on (ZIP, DOB, sex). One row collapses to a single
    individual; the closing line is the 87% uniqueness statistic.
  - RandomizedResponseCoinGrid: 100 dots, each with a hidden truth bit; each
    flips a coin and answers either truth or a random bit; the aggregate count
    is de-shifted by the unbiased estimator into the true rate.
  - DefinitionAsGame: the load-bearing scene. Two neighboring databases, a
    mechanism, two output distributions; a vertical scan reveals the e^eps
    bound on their ratio. Stage-based with FadeOut between beats.
  - PrivacyBudgetLedger: a budget meter drains as queries land. Toggle from
    sequential composition (linear drain) to advanced composition (sqrt drain
    with a small delta meter ticking up).

House rule: all narrative text lives at the top or bottom edge, never centre.
Inline labels attach to specific graphical objects only.

Layout safe zones (default Manim frame is 14.222 wide × 8.0 tall):
  - Header band:      y in [+3.0, +4.0]
  - Main stage:       y in [-3.0, +2.8]
  - Bottom narrative: y in [-3.8, -3.4]
  - Horizontal:       x in [-7.0, +7.0]  (keep wide labels well inside)
"""

from manim import *
import numpy as np


# ──────────────────────────────────────────────
# Shared palette (matches post_03)
# ──────────────────────────────────────────────
COLORS = [BLUE, GREEN, ORANGE, PURPLE, RED]
BG_COLOR = "#0f0f1a"
ACCENT = "#f0b429"
SOFT_WHITE = "#e0e0e8"
DIM_WHITE = "#888898"
MEMBER_COLOR = "#ff6b6b"      # red — adversary / attack side
NONMEMBER_COLOR = "#4ecdc4"   # teal — curator / defender side
TAIL_COLOR = "#c084fc"        # purple — singleton / individual highlight
TRUTH_YES = "#ff6b6b"
TRUTH_NO = "#4ecdc4"


def _header(title: str, subtitle: str) -> VGroup:
    t = Text(title, font_size=34, color=SOFT_WHITE)
    s = Text(subtitle, font_size=18, color=DIM_WHITE)
    return VGroup(t, s).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.3)


def _bottom(msg: str, color=SOFT_WHITE, font_size=20) -> Text:
    return Text(msg, font_size=font_size, color=color).to_edge(DOWN, buff=0.4)


# ══════════════════════════════════════════════════════════════════
# Scene 1 — SweenyJoinAttack
# ══════════════════════════════════════════════════════════════════
class SweenyJoinAttack(Scene):
    """Two tables, joined on quasi-identifiers, collapse one row to one person."""

    def construct(self):
        self.camera.background_color = BG_COLOR

        header = _header("Anonymized, Until Joined", "two public datasets, three shared columns")
        self.play(FadeIn(header), run_time=0.6)

        # ───────── Beat 1: build the two tables ─────────
        cell_w, cell_h = 0.9, 0.42

        def make_cell(text, color=SOFT_WHITE, fill=None, font_size=14, weight=NORMAL):
            box = Rectangle(
                width=cell_w, height=cell_h,
                color=GREY_D, stroke_width=1,
                fill_color=fill if fill else BG_COLOR,
                fill_opacity=0.0 if fill is None else 0.4,
            )
            t = Text(str(text), font_size=font_size, color=color, weight=weight).move_to(box.get_center())
            return VGroup(box, t)

        # Hospital records (left), name redacted, but ZIP/DOB/Sex/Diagnosis visible
        left_headers = ["[redacted]", "ZIP", "DOB", "sex", "diagnosis"]
        left_rows = [
            ["#0014", "02139", "1945-07", "M", "asthma"],
            ["#0023", "02141", "1962-03", "F", "anxiety"],
            ["#0031", "02138", "1945-07", "M", "hypertension"],
            ["#0042", "02140", "1971-11", "F", "migraine"],
            ["#0058", "02139", "1958-04", "F", "diabetes"],
        ]
        target_row_idx = 2  # the one we'll re-identify

        left_table = VGroup()
        for j, h in enumerate(left_headers):
            cell = make_cell(h, color=NONMEMBER_COLOR, font_size=13, weight=BOLD,
                             fill=NONMEMBER_COLOR)
            cell.move_to(np.array([j * cell_w, 0, 0]))
            left_table.add(cell)
        for i, row in enumerate(left_rows):
            for j, v in enumerate(row):
                cell = make_cell(v, color=SOFT_WHITE, font_size=13)
                cell.move_to(np.array([j * cell_w, -(i + 1) * cell_h, 0]))
                left_table.add(cell)
        left_table.scale(0.9).to_edge(LEFT, buff=0.4).shift(DOWN * 0.3)

        # Voter roll (right): name + ZIP + DOB + sex
        right_headers = ["name", "ZIP", "DOB", "sex"]
        right_rows = [
            ["A. Patel", "02139", "1945-07", "M"],
            ["B. Chen", "02141", "1962-03", "F"],
            ["W. Weld",  "02138", "1945-07", "M"],
            ["D. Kim",   "02140", "1971-11", "F"],
            ["E. Park",  "02139", "1958-04", "F"],
        ]
        right_table = VGroup()
        for j, h in enumerate(right_headers):
            cell = make_cell(h, color=MEMBER_COLOR, font_size=13, weight=BOLD,
                             fill=MEMBER_COLOR)
            cell.move_to(np.array([j * cell_w, 0, 0]))
            right_table.add(cell)
        for i, row in enumerate(right_rows):
            for j, v in enumerate(row):
                cell = make_cell(v, color=SOFT_WHITE, font_size=13)
                cell.move_to(np.array([j * cell_w, -(i + 1) * cell_h, 0]))
                right_table.add(cell)
        right_table.scale(0.9).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.3)

        left_tag = Text("Anonymized hospital records",
                        font_size=16, color=NONMEMBER_COLOR).next_to(left_table, UP, buff=0.2)
        right_tag = Text("Public voter roll  ($20)",
                         font_size=16, color=MEMBER_COLOR).next_to(right_table, UP, buff=0.2)

        b1 = _bottom("Two datasets. Each is harmless on its own.", color=SOFT_WHITE)
        self.play(
            FadeIn(left_table), FadeIn(right_table),
            FadeIn(left_tag), FadeIn(right_tag),
            FadeIn(b1), run_time=1.1,
        )
        self.wait(0.6)

        # ───────── Beat 2: highlight the shared columns (ZIP, DOB, sex) ─────────
        def left_col_cells(j):
            base = 5  # headers
            return [left_table[base + i * 5 + j] for i in range(5)] + [left_table[j]]

        def right_col_cells(j):
            base = 4
            return [right_table[base + i * 4 + j] for i in range(5)] + [right_table[j]]

        highlight_left = VGroup(*[c for j in (1, 2, 3) for c in left_col_cells(j)])
        highlight_right = VGroup(*[c for j in (1, 2, 3) for c in right_col_cells(j)])

        b2 = _bottom("Three columns appear in both: ZIP, DOB, sex.", color=ACCENT)
        self.play(
            ReplacementTransform(b1, b2),
            *[c[0].animate.set_stroke(ACCENT, width=2.5) for c in highlight_left],
            *[c[0].animate.set_stroke(ACCENT, width=2.5) for c in highlight_right],
            run_time=0.9,
        )
        self.wait(0.6)

        # ───────── Beat 3: the join — arrows from one row to one row ─────────
        left_target_idx = target_row_idx  # 2
        right_target_idx = 2

        left_target_cells = [left_table[5 + left_target_idx * 5 + j] for j in range(5)]
        right_target_cells = [right_table[4 + right_target_idx * 4 + j] for j in range(4)]

        self.play(
            *[c[0].animate.set_fill(ACCENT, opacity=0.18).set_stroke(ACCENT, width=2.5)
              for c in left_target_cells],
            *[c[0].animate.set_fill(ACCENT, opacity=0.18).set_stroke(ACCENT, width=2.5)
              for c in right_target_cells],
            run_time=0.6,
        )

        arrows = VGroup()
        for j in (1, 2, 3):
            l_cell = left_target_cells[j][0]
            r_cell = right_target_cells[j][0]
            a = CurvedArrow(
                l_cell.get_right(), r_cell.get_left(),
                color=ACCENT, stroke_width=2,
                tip_length=0.15, angle=-PI / 4 + (j - 2) * 0.15,
            )
            arrows.add(a)

        b3 = _bottom("Join the rows that match on all three.", color=ACCENT)
        self.play(ReplacementTransform(b2, b3), Create(arrows), run_time=0.9)
        self.wait(0.7)

        # ───────── Beat 4: reveal the name on the diagnosis ─────────
        joined_name = right_target_cells[0][1].copy()
        joined_diag = left_target_cells[4][1].copy()

        reveal_pos = ORIGIN + DOWN * 2.6
        reveal = VGroup(
            Text("W. Weld", font_size=28, color=ACCENT, weight=BOLD),
            Text(":", font_size=28, color=SOFT_WHITE),
            Text("hypertension", font_size=26, color=ACCENT),
        ).arrange(RIGHT, buff=0.2).move_to(reveal_pos)

        b4 = _bottom("One join.  One person.  One private fact.", color=ACCENT, font_size=22)
        self.play(
            ReplacementTransform(b3, b4),
            Transform(joined_name, reveal[0]),
            FadeIn(reveal[1]),
            Transform(joined_diag, reveal[2]),
            run_time=1.0,
        )
        self.wait(1.4)

        b5 = _bottom("(ZIP, DOB, sex) uniquely identifies 87% of Americans.",
                     color=ACCENT, font_size=22)
        self.play(ReplacementTransform(b4, b5), run_time=0.6)
        self.wait(2.5)


# ══════════════════════════════════════════════════════════════════
# Scene 2 — RandomizedResponseCoinGrid  (rewritten layout)
# ══════════════════════════════════════════════════════════════════
class RandomizedResponseCoinGrid(Scene):
    """100 dots, each a hidden truth. Each flips a coin and reports either
    truth or a random bit. Stage 3 fades the grid down so the estimator
    equation has the full lower stage to itself.

    Layout:
      - header           y ≈ +3.5
      - 10×10 grid       centred at LEFT*2.6 + UP*0.5  → spans roughly y[-1.0, +2.0]
      - right panel      centred at RIGHT*3.4         → labels stacked vertically
      - estimator eq     y ≈ -2.3
      - bottom narrative y ≈ -3.6
    """

    def construct(self):
        self.camera.background_color = BG_COLOR

        header = _header("Plausible Deniability, On Paper",
                         "the estimator that undoes the noise in expectation")
        self.play(FadeIn(header), run_time=0.6)

        # ───────── Beat 1: 10×10 grid of truth dots ─────────
        rows, cols = 10, 10
        n = rows * cols
        true_p = 0.30
        rng = np.random.default_rng(7)
        truths = (rng.uniform(size=n) < true_p).astype(int)
        true_yes = int(truths.sum())

        spacing = 0.32
        grid_w = (cols - 1) * spacing
        grid_h = (rows - 1) * spacing
        grid_centre = LEFT * 2.6 + UP * 0.5

        dots = VGroup()
        for i in range(n):
            r, c = i // cols, i % cols
            x = grid_centre[0] - grid_w / 2 + c * spacing
            y = grid_centre[1] - grid_h / 2 + (rows - 1 - r) * spacing
            dot = Dot(point=np.array([x, y, 0]), radius=0.10,
                      color=TRUTH_YES if truths[i] else TRUTH_NO,
                      fill_opacity=0.85)
            dots.add(dot)

        # Right-side panel (anchor at RIGHT*3.4 keeps widest text inside the frame)
        legend = VGroup(
            VGroup(Dot(color=TRUTH_YES, radius=0.09),
                   Text("yes", font_size=14, color=SOFT_WHITE)
                   ).arrange(RIGHT, buff=0.15),
            VGroup(Dot(color=TRUTH_NO, radius=0.09),
                   Text("no",  font_size=14, color=SOFT_WHITE)
                   ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        truth_lbl = Text(f"true rate p = {true_yes/100:.2f}",
                         font_size=18, color=SOFT_WHITE)

        right_panel = VGroup(legend, truth_lbl).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        right_panel.move_to(RIGHT * 3.4 + UP * 1.2)

        b1 = _bottom("Each person has a private truth.", color=SOFT_WHITE)
        self.play(
            FadeIn(dots, lag_ratio=0.005),
            FadeIn(right_panel),
            FadeIn(b1),
            run_time=1.2,
        )
        self.wait(0.6)

        # ───────── Beat 2: flip the coin; dots change colour in waves ─────────
        coins = rng.uniform(size=n)
        rerolls = rng.uniform(size=n)
        keep_truth = coins < 0.5
        reported = np.where(keep_truth, truths, (rerolls < 0.5).astype(int))
        reported_yes = int(reported.sum())

        b2 = _bottom("Heads: tell the truth.  Tails: flip again, answer at random.",
                     color=ACCENT, font_size=20)
        self.play(ReplacementTransform(b1, b2), run_time=0.5)

        for wave in range(rows):
            anims = []
            for c in range(cols):
                i = wave * cols + c
                target_color = TRUTH_YES if reported[i] else TRUTH_NO
                anims.append(dots[i].animate.set_color(target_color))
            self.play(*anims, run_time=0.18)
        self.wait(0.4)

        reported_lbl = Text(f"reported rate = {reported_yes/100:.2f}",
                            font_size=18, color=DIM_WHITE)
        reported_lbl.next_to(truth_lbl, DOWN, aligned_edge=LEFT, buff=0.25)
        self.play(FadeIn(reported_lbl), run_time=0.4)
        self.wait(0.4)

        # ───────── Beat 3: dim the grid; reveal the estimator at the bottom ─────────
        b3 = _bottom("Each individual answer is deniable.  The aggregate is recoverable.",
                     color=ACCENT, font_size=20)
        self.play(
            ReplacementTransform(b2, b3),
            dots.animate.set_opacity(0.22),
            run_time=0.7,
        )

        eq = MathTex(
            r"\Pr[\text{yes}]\,=\,\tfrac{1}{2}\,p\,+\,\tfrac{1}{4}",
            r"\quad\Rightarrow\quad",
            r"\hat{p}\,=\,2\,\Pr[\text{yes}]\,-\,\tfrac{1}{2}",
            font_size=26,
            color=SOFT_WHITE,
        )
        eq[2].set_color(ACCENT)
        eq.move_to(DOWN * 2.4)

        self.play(FadeIn(eq, shift=UP * 0.2), run_time=0.7)
        self.wait(0.6)

        p_hat = max(0.0, min(1.0, 2 * (reported_yes / 100) - 0.5))
        recovery_lbl = Text(
            f"p̂ = 2·{reported_yes/100:.2f} − 0.5 = {p_hat:.2f}",
            font_size=18, color=ACCENT,
        )
        recovery_lbl.next_to(reported_lbl, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(FadeIn(recovery_lbl), run_time=0.4)
        self.wait(2.5)


# ══════════════════════════════════════════════════════════════════
# Scene 3 — DefinitionAsGame  (rewritten — stage-based with FadeOut)
# ══════════════════════════════════════════════════════════════════
class DefinitionAsGame(Scene):
    """The post's spine. Three stages, each clearing prior content:
      Stage 1: D and D' side-by-side at top, mechanism and curves arriving below.
      Stage 2: a vertical scan across the two output curves shows the
               density ratio bounded by e^eps.
      Stage 3: the definition equation lands at the bottom.

    Layout y-band budget:
      - header                  +3.5
      - dbs row centre          +1.5  (boxes 1.7 tall → spans +0.65 to +2.35)
      - mech / output_axes      around y = -0.6  (axes y_length=1.6 → spans -1.4 to +0.2)
      - equation                -2.5
      - bottom narrative        -3.6
    """

    def construct(self):
        self.camera.background_color = BG_COLOR

        header = _header("The Game", "the bound that caps an adversary's best test")
        self.play(FadeIn(header), run_time=0.6)

        # ──────────── STAGE 1: build the two databases ────────────
        def make_db(label, rows, color, anchor):
            box = RoundedRectangle(width=2.0, height=1.7, corner_radius=0.10,
                                   color=color, stroke_width=2,
                                   fill_color="#1a1a2e", fill_opacity=0.5)
            content = VGroup(*[Text(r, font_size=14, color=SOFT_WHITE) for r in rows])
            content.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
            content.move_to(box.get_center())
            tag = Text(label, font_size=22, color=color, weight=BOLD).next_to(box, UP, buff=0.10)
            grp = VGroup(box, tag, content)
            grp.move_to(anchor)
            return grp, content

        rows_D  = ["• Bao", "• Chen", "• Diallo", "• Eve", "• Anna"]
        rows_Dp = ["• Bao", "• Chen", "• Diallo", "• Eve"]
        db_D, content_D  = make_db("D",  rows_D,  NONMEMBER_COLOR, LEFT * 4.6 + UP * 1.5)
        db_Dp, _         = make_db("D'", rows_Dp, MEMBER_COLOR,    LEFT * 1.8 + UP * 1.5)
        content_D[-1].set_color(TAIL_COLOR)  # Anna in pink

        diff_label = Text("differ in 1 row (Anna)", font_size=14, color=TAIL_COLOR)
        diff_label.move_to(np.array([(db_D.get_center()[0] + db_Dp.get_center()[0]) / 2,
                                     0.35, 0]))

        b1 = _bottom("Two databases.  Differ by exactly one row.", color=SOFT_WHITE)
        self.play(FadeIn(db_D), FadeIn(db_Dp), FadeIn(b1), run_time=1.0)
        self.play(FadeIn(diff_label), run_time=0.4)
        self.wait(0.5)

        # Mechanism box and output axes appear on the right and below
        mech_box = RoundedRectangle(width=1.4, height=0.9, corner_radius=0.10,
                                    color=ACCENT, stroke_width=2,
                                    fill_color="#1a1a2e", fill_opacity=0.5)
        mech_label = Text("M", font_size=26, color=ACCENT, weight=BOLD).move_to(mech_box.get_center())
        mech = VGroup(mech_box, mech_label).move_to(RIGHT * 2.5 + UP * 1.5)

        output_axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 0.8, 0.2],
            x_length=4.0, y_length=1.6,
            axis_config={"color": GREY_B, "include_tip": False, "font_size": 14},
        ).move_to(RIGHT * 2.5 + DOWN * 0.6)

        def dist_D(x):  return 0.6 * np.exp(-((x - 2.2) ** 2) / 0.7)
        def dist_Dp(x): return 0.6 * np.exp(-((x - 2.5) ** 2) / 0.7)

        curve_D  = output_axes.plot(dist_D,  x_range=[0, 5], color=NONMEMBER_COLOR, stroke_width=2.5)
        curve_Dp = output_axes.plot(dist_Dp, x_range=[0, 5], color=MEMBER_COLOR,   stroke_width=2.5)

        # Connecting arrows: dbs → mech → output_axes
        in_arrow_D  = Arrow(db_D.get_right(),  mech.get_left(),
                            color=NONMEMBER_COLOR, stroke_width=2, buff=0.15, tip_length=0.15)
        in_arrow_Dp = Arrow(db_Dp.get_right(), mech.get_left(),
                            color=MEMBER_COLOR, stroke_width=2, buff=0.15, tip_length=0.15)
        out_arrow = Arrow(mech.get_bottom(), output_axes.get_top() + UP * 0.05,
                          color=ACCENT, stroke_width=2, buff=0.10, tip_length=0.15)

        b2 = _bottom("Curator picks one secretly, runs M, sends the output.", color=SOFT_WHITE)
        self.play(ReplacementTransform(b1, b2), run_time=0.5)
        self.play(FadeIn(mech), Create(in_arrow_D), Create(in_arrow_Dp), run_time=0.7)
        self.play(Create(out_arrow), Create(output_axes), run_time=0.8)
        self.play(Create(curve_D), Create(curve_Dp), run_time=1.0)

        out_lbl_D  = Text("M(D)",  font_size=14, color=NONMEMBER_COLOR).next_to(
            output_axes.c2p(2.2, dist_D(2.2)), UP, buff=0.05)
        out_lbl_Dp = Text("M(D')", font_size=14, color=MEMBER_COLOR).next_to(
            output_axes.c2p(2.5, dist_Dp(2.5)), UP, buff=0.05)
        self.play(FadeIn(out_lbl_D), FadeIn(out_lbl_Dp), run_time=0.4)
        self.wait(0.5)

        # ──────────── STAGE 2: clear setup, sweep ratio across the curves ────────────
        b3 = _bottom("At every output value, the ratio of the two densities is at most e^ε.",
                     color=ACCENT, font_size=20)
        self.play(
            ReplacementTransform(b2, b3),
            FadeOut(db_D), FadeOut(db_Dp), FadeOut(diff_label),
            FadeOut(mech), FadeOut(in_arrow_D), FadeOut(in_arrow_Dp), FadeOut(out_arrow),
            run_time=0.8,
        )

        # Move + enlarge the output axes to the centre top
        new_axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 0.8, 0.2],
            x_length=8.0, y_length=2.4,
            axis_config={"color": GREY_B, "include_tip": False, "font_size": 16},
        ).move_to(UP * 0.8)
        new_curve_D  = new_axes.plot(dist_D,  x_range=[0, 5], color=NONMEMBER_COLOR, stroke_width=3)
        new_curve_Dp = new_axes.plot(dist_Dp, x_range=[0, 5], color=MEMBER_COLOR,   stroke_width=3)
        new_lbl_D  = Text("M(D)",  font_size=16, color=NONMEMBER_COLOR).next_to(
            new_axes.c2p(2.2, dist_D(2.2)), UP, buff=0.08)
        new_lbl_Dp = Text("M(D')", font_size=16, color=MEMBER_COLOR).next_to(
            new_axes.c2p(2.5, dist_Dp(2.5)), UP, buff=0.08)

        self.play(
            ReplacementTransform(output_axes, new_axes),
            ReplacementTransform(curve_D,  new_curve_D),
            ReplacementTransform(curve_Dp, new_curve_Dp),
            ReplacementTransform(out_lbl_D,  new_lbl_D),
            ReplacementTransform(out_lbl_Dp, new_lbl_Dp),
            run_time=0.9,
        )

        # Vertical scan line + a moving "ratio ≤ e^ε" tag near the top of the chart
        scan = DashedLine(
            new_axes.c2p(0.5, 0), new_axes.c2p(0.5, 0.78),
            color=ACCENT, stroke_width=2,
        )
        ratio_tag = Text("ratio ≤ e^ε", font_size=16, color=ACCENT)
        ratio_tag.next_to(scan, UP, buff=0.05)

        self.play(Create(scan), FadeIn(ratio_tag), run_time=0.5)

        # Sweep
        target_x = 4.2
        self.play(
            scan.animate.move_to(np.array([new_axes.c2p(target_x, 0)[0],
                                           scan.get_center()[1], 0])),
            ratio_tag.animate.move_to(np.array([new_axes.c2p(target_x, 0)[0],
                                                ratio_tag.get_center()[1], 0])),
            run_time=2.0, rate_func=linear,
        )
        self.wait(0.4)

        # ──────────── STAGE 3: state the definition ────────────
        b4 = _bottom("Differential privacy is the bound that caps the game.",
                     color=ACCENT, font_size=22)
        eq = MathTex(
            r"\Pr[M(D)\in S]\,\le\,e^{\varepsilon}\,\Pr[M(D')\in S]",
            font_size=30, color=ACCENT,
        ).move_to(DOWN * 2.5)

        self.play(
            ReplacementTransform(b3, b4),
            FadeIn(eq, shift=UP * 0.2),
            run_time=0.8,
        )
        self.wait(2.8)


# ══════════════════════════════════════════════════════════════════
# Scene 4 — PrivacyBudgetLedger  (rewritten — clean vertical zoning)
# ══════════════════════════════════════════════════════════════════
class PrivacyBudgetLedger(Scene):
    """Five queries, ε=1 each, hit a budget meter. First in the sequential
    regime (linear drain to ε=5). Then reset and replay in the advanced
    regime (drain ≈ √(2k ln(1/δ))·ε ≈ 4.8) — the first place δ pays for itself.

    Layout zoning:
      - header                +3.5
      - regime label          +2.3
      - meter                  +1.2
      - meter side labels      +1.2  (left/right of meter)
      - query label (transient) +0.3
      - δ meter row           -0.7
      - formula               -1.7
      - bottom narrative      -3.6
    """

    def construct(self):
        self.camera.background_color = BG_COLOR

        header = _header("A Budget That Drains",
                         "every query you publish costs you privacy")
        self.play(FadeIn(header), run_time=0.6)

        # ───────── Geometry ─────────
        budget_total = 10.0
        meter_w, meter_h = 7.0, 0.55
        meter_y = 1.2

        meter_outline = Rectangle(width=meter_w, height=meter_h,
                                  color=GREY_B, stroke_width=2)
        meter_outline.move_to(np.array([0, meter_y, 0]))

        meter_left = meter_outline.get_left()[0]

        meter_lhs = Text("ε spent", font_size=16, color=SOFT_WHITE).next_to(meter_outline, LEFT, buff=0.25)
        meter_rhs = Text("budget = 10", font_size=16, color=DIM_WHITE).next_to(meter_outline, RIGHT, buff=0.25)

        # Regime label sits above the meter, centred
        regime_label = Text("regime: sequential", font_size=18, color=NONMEMBER_COLOR)
        regime_label.move_to(np.array([0, 2.3, 0]))

        # δ meter: a small rectangle one row below the budget meter (own zone)
        delta_outline = Rectangle(width=2.2, height=0.22, color=GREY_B, stroke_width=1.5)
        delta_outline.move_to(np.array([0, -0.7, 0]))
        delta_lhs = Text("δ", font_size=14, color=DIM_WHITE).next_to(delta_outline, LEFT, buff=0.2)
        delta_rhs = Text("(catastrophic-failure prob.)", font_size=12, color=DIM_WHITE).next_to(delta_outline, RIGHT, buff=0.2)

        b1 = _bottom("Five queries, each ε = 1.  How much budget did we spend?",
                     color=SOFT_WHITE)
        self.play(
            FadeIn(meter_outline), FadeIn(meter_lhs), FadeIn(meter_rhs),
            FadeIn(regime_label),
            FadeIn(delta_outline), FadeIn(delta_lhs), FadeIn(delta_rhs),
            FadeIn(b1),
            run_time=0.9,
        )
        self.wait(0.4)

        # ───────── Beat 1: sequential composition (5 queries × ε=1 each) ─────────
        n_queries = 5
        per_query = 1.0
        spent = 0.0
        bars_seq = VGroup()

        for k in range(n_queries):
            chunk_w = meter_w * (per_query / budget_total)
            chunk = Rectangle(
                width=chunk_w, height=meter_h - 0.04,
                color=NONMEMBER_COLOR, fill_color=NONMEMBER_COLOR,
                fill_opacity=0.7, stroke_width=0,
            )
            chunk.move_to(np.array([
                meter_left + meter_w * spent / budget_total + chunk_w / 2,
                meter_y, 0,
            ]))
            bars_seq.add(chunk)

            query_label = Text(f"query {k+1}: ε = 1", font_size=16, color=ACCENT).move_to(
                np.array([0, 0.3, 0])
            )
            self.play(FadeIn(query_label, shift=UP * 0.1), run_time=0.18)
            self.play(GrowFromEdge(chunk, LEFT), run_time=0.30)
            self.play(FadeOut(query_label), run_time=0.12)
            spent += per_query

        b2 = _bottom("Sequential composition: ε's add.  Five queries spent ε = 5.",
                     color=ACCENT, font_size=20)
        self.play(ReplacementTransform(b1, b2), run_time=0.6)
        self.wait(1.4)

        # ───────── Beat 2: switch regime, replay queries with the advanced bound ─────────
        delta_value = 1e-5
        adv_total = float(np.sqrt(2 * n_queries * np.log(1 / delta_value)))

        new_regime = Text("regime: advanced (with δ)", font_size=18, color=ACCENT)
        new_regime.move_to(regime_label.get_center())

        b3 = _bottom("Now allow a tiny δ.  Replay the same five queries.",
                     color=SOFT_WHITE)
        self.play(
            ReplacementTransform(b2, b3),
            ReplacementTransform(regime_label, new_regime),
            FadeOut(bars_seq),
            run_time=0.8,
        )
        self.wait(0.3)

        chunk_w = meter_w * (adv_total / budget_total)
        adv_bar = Rectangle(
            width=chunk_w, height=meter_h - 0.04,
            color=ACCENT, fill_color=ACCENT, fill_opacity=0.7, stroke_width=0,
        )
        adv_bar.move_to(np.array([meter_left + chunk_w / 2, meter_y, 0]))

        # Sub-ticks marking each of the 5 queries inside the advanced bar
        ticks = VGroup()
        for k in range(n_queries):
            tick_x = meter_left + chunk_w * (k + 1) / n_queries
            tick = Line(
                start=np.array([tick_x, meter_y - meter_h / 2 + 0.03, 0]),
                end=np.array([tick_x, meter_y + meter_h / 2 - 0.03, 0]),
                color=BG_COLOR, stroke_width=1.5,
            )
            ticks.add(tick)

        self.play(GrowFromEdge(adv_bar, LEFT), run_time=1.0)
        self.play(FadeIn(ticks), run_time=0.4)

        # δ meter ticks up a small amount (same bar fills inside the δ outline)
        delta_fill = Rectangle(
            width=delta_outline.width * 0.06, height=delta_outline.height - 0.04,
            color=ACCENT, fill_color=ACCENT, fill_opacity=0.7, stroke_width=0,
        )
        delta_fill.move_to(np.array([
            delta_outline.get_left()[0] + delta_outline.width * 0.03,
            delta_outline.get_center()[1], 0,
        ]))
        self.play(GrowFromEdge(delta_fill, LEFT), run_time=0.5)

        # Formula: lower zone, well clear of both the δ meter and the bottom narrative
        formula = MathTex(
            r"\varepsilon_{\text{tot}}\,\approx\,\sqrt{2\,k\,\ln(1/\delta)}\,\cdot\,\varepsilon",
            font_size=26, color=ACCENT,
        ).move_to(np.array([0, -1.7, 0]))

        b4 = _bottom(
            f"Advanced composition: total ε ≈ {adv_total:.1f}, not 5.  δ buys you the savings.",
            color=ACCENT, font_size=20,
        )
        self.play(
            ReplacementTransform(b3, b4),
            FadeIn(formula, shift=UP * 0.15),
            run_time=0.8,
        )
        self.wait(2.6)


# ══════════════════════════════════════════════════════════════════
# (no Scene 5 — the post's fifth visual is a Plotly figure embedded in
#  the qmd code cell, EpsilonPosteriorDial. See posts/04-differential-privacy
#  /index.qmd for the figure source.)
# ══════════════════════════════════════════════════════════════════
