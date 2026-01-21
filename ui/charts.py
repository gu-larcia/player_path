"""Plotly chart builders for player analytics."""

import plotly.graph_objects as go
from typing import Dict, List, Any
import pandas as pd
import math

from config import COLORS, SKILL_CATEGORIES


def create_skill_radar(skills: Dict[str, Any], categories: Dict[str, List[str]] = None) -> go.Figure:
    """Create a radar chart showing skill category distribution."""
    if categories is None:
        categories = SKILL_CATEGORIES
    
    category_names = []
    category_scores = []
    
    max_possible_xp = 200_000_000
    
    for cat_name, skill_names in categories.items():
        total_xp = sum(
            skills[s].experience 
            for s in skill_names 
            if s in skills
        )
        max_xp = max_possible_xp * len(skill_names)
        if total_xp > 0:
            score = math.log10(total_xp + 1) / math.log10(max_xp + 1) * 100
        else:
            score = 0
        
        category_names.append(cat_name)
        category_scores.append(score)
    
    category_names.append(category_names[0])
    category_scores.append(category_scores[0])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=category_scores,
        theta=category_names,
        fill='toself',
        fillcolor='rgba(212, 175, 55, 0.2)',
        line=dict(color=COLORS["primary"], width=2),
        name='Skills'
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor=COLORS["background"],
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False,
                gridcolor='rgba(136, 136, 136, 0.3)',
            ),
            angularaxis=dict(
                gridcolor='rgba(136, 136, 136, 0.3)',
                linecolor='rgba(136, 136, 136, 0.3)',
            ),
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=60, r=60, t=40, b=40),
        font=dict(color=COLORS["text"], family="Nunito"),
        height=350,
    )
    
    return fig


def create_playstyle_bars(scores: Dict[str, float]) -> go.Figure:
    """Create horizontal bar chart for playstyle dimensions."""
    
    labels = {
        "skiller_vs_pvmer": "Skiller ← → PvMer",
        "boss_diversity": "Boss Diversity",
        "raid_focus": "Raid Focus", 
        "skill_balance": "Skill Balance",
        "combat_focus": "Combat Focus",
    }
    
    names = []
    values = []
    
    for key, label in labels.items():
        if key in scores:
            names.append(label)
            values.append(scores[key])
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=names,
        x=values,
        orientation='h',
        marker=dict(
            color=values,
            colorscale=[[0, COLORS["secondary"]], [1, COLORS["primary"]]],
        ),
        text=[f'{v:.0f}' for v in values],
        textposition='inside',
        textfont=dict(color='white', size=12),
    ))
    
    fig.update_layout(
        xaxis=dict(
            range=[0, 100],
            showgrid=True,
            gridcolor='rgba(136, 136, 136, 0.2)',
            title=None,
        ),
        yaxis=dict(
            title=None,
            autorange="reversed",
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=120, r=20, t=20, b=40),
        font=dict(color=COLORS["text"], family="Nunito"),
        height=250,
    )
    
    return fig


def create_boss_distribution(bosses: Dict[str, Any], top_n: int = 10) -> go.Figure:
    """Create horizontal bar chart of top bosses by KC."""
    
    boss_data = [
        (b.display_name, b.kills)
        for b in bosses.values()
        if b.kills > 0
    ]
    boss_data.sort(key=lambda x: x[1], reverse=True)
    boss_data = boss_data[:top_n]
    
    if not boss_data:
        fig = go.Figure()
        fig.add_annotation(
            text="No boss kills recorded",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(color=COLORS["muted"], size=14),
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300,
        )
        return fig
    
    names, values = zip(*boss_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=names,
        x=values,
        orientation='h',
        marker=dict(color=COLORS["combat"]),
        text=[f'{v:,}' for v in values],
        textposition='outside',
        textfont=dict(color=COLORS["text"], size=11),
    ))
    
    fig.update_layout(
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(136, 136, 136, 0.2)',
            title="Kill Count",
        ),
        yaxis=dict(
            title=None,
            autorange="reversed",
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=150, r=60, t=20, b=40),
        font=dict(color=COLORS["text"], family="Nunito"),
        height=max(200, len(boss_data) * 35 + 60),
    )
    
    return fig


def create_skill_distribution(skills: Dict[str, Any]) -> go.Figure:
    """Create treemap showing skill XP distribution."""
    
    labels = []
    parents = []
    values = []
    colors = []
    
    category_colors = {
        "Combat": COLORS["combat"],
        "Gathering": COLORS["gathering"],
        "Artisan": COLORS["artisan"],
        "Support": COLORS["support"],
    }
    
    labels.append("Total XP")
    parents.append("")
    values.append(0)
    colors.append(COLORS["surface"])
    
    for cat_name, skill_names in SKILL_CATEGORIES.items():
        cat_xp = sum(
            skills[s].experience 
            for s in skill_names 
            if s in skills
        )
        labels.append(cat_name)
        parents.append("Total XP")
        values.append(cat_xp)
        colors.append(category_colors.get(cat_name, COLORS["muted"]))
        
        for skill in skill_names:
            if skill in skills and skills[skill].experience > 0:
                labels.append(skill.title())
                parents.append(cat_name)
                values.append(skills[skill].experience)
                colors.append(category_colors.get(cat_name, COLORS["muted"]))
    
    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(colors=colors),
        textinfo="label+percent parent",
        hovertemplate="<b>%{label}</b><br>XP: %{value:,.0f}<extra></extra>",
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(color="white", family="Nunito"),
        height=400,
    )
    
    return fig


def create_journey_timeline(timeline: List[Dict], milestones: List[Dict] = None) -> go.Figure:
    """Create timeline chart showing player progression."""
    
    if not timeline:
        fig = go.Figure()
        fig.add_annotation(
            text="Insufficient historical data for timeline",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(color=COLORS["muted"], size=14),
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300,
        )
        return fig
    
    df = pd.DataFrame(timeline)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["total_level"],
        mode='lines+markers',
        name='Total Level',
        line=dict(color=COLORS["primary"], width=2),
        marker=dict(size=6),
        hovertemplate="<b>%{x|%Y-%m-%d}</b><br>Total Level: %{y:,}<extra></extra>",
    ))
    
    if milestones:
        for m in milestones:
            fig.add_vline(
                x=m["date"],
                line=dict(color=COLORS["primary"], width=1, dash="dot"),
                annotation_text=m["description"][:20],
                annotation_position="top",
            )
    
    fig.update_layout(
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(136, 136, 136, 0.2)',
            title=None,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(136, 136, 136, 0.2)',
            title="Total Level",
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=60, r=20, t=40, b=40),
        font=dict(color=COLORS["text"], family="Nunito"),
        height=350,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )
    
    return fig


def create_ehp_ehb_gauge(ehp: float, ehb: float) -> go.Figure:
    """Create a dual gauge showing EHP and EHB."""
    
    fig = go.Figure()
    
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=ehp,
        title={'text': "EHP", 'font': {'size': 14}},
        gauge={
            'axis': {'range': [0, max(5000, ehp * 1.2)]},
            'bar': {'color': COLORS["gathering"]},
            'bgcolor': COLORS["surface"],
            'bordercolor': COLORS["muted"],
        },
        domain={'x': [0, 0.45], 'y': [0, 1]},
        number={'font': {'size': 24, 'color': COLORS["text"]}},
    ))
    
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=ehb,
        title={'text': "EHB", 'font': {'size': 14}},
        gauge={
            'axis': {'range': [0, max(1000, ehb * 1.2)]},
            'bar': {'color': COLORS["combat"]},
            'bgcolor': COLORS["surface"],
            'bordercolor': COLORS["muted"],
        },
        domain={'x': [0.55, 1], 'y': [0, 1]},
        number={'font': {'size': 24, 'color': COLORS["text"]}},
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS["text"], family="Nunito"),
        height=200,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    
    return fig
