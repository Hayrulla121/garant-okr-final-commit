import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import pandas as pd
import json
import uuid
import os
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

TRANSLATIONS = {
    "en": {
        "title": "OKR Performance Tracker",
        "performance_scale": "Performance Scale",
        "department": "Department",
        "department_name": "Department Name",
        "create_department": "➕ Create New Department",
        "select_department": "Select Department",
        "delete_department": "🗑️ Delete Department",
        "no_departments": "No departments. Create one first!",
        "create_objective": "➕ Create New Objective",
        "objective_name": "Objective Name",
        "objective": "Objective",
        "add_key_results": "Add Key Results",
        "kr_name": "KR Name",
        "kr_description": "Description (hover tooltip)",
        "kr_description_placeholder": "Enter meaning/description of this KR...",
        "type": "Type",
        "higher_better": "↑ Higher is better",
        "lower_better": "↓ Lower is better",
        "unit": "Unit",
        "thresholds": "Thresholds",
        "add_kr": "➕ Add KR",
        "added_krs": "Added Key Results",
        "remove": "Remove",
        "create": "✅ Create Objective",
        "enter_name_error": "Enter objective name and add at least one KR",
        "score": "🎯 Score",
        "add_kr_to_obj": "➕ Add KR to this Objective",
        "add": "➕ Add",
        "delete_objective": "🗑️ Delete Objective",
        "export_json": "Export JSON",
        "export_excel": "Export Excel",
        "save_data": "Save Data",
        "load_data": "📂 Load Data",
        "data_saved": "✅ Data saved!",
        "data_loaded": "✅ Data loaded!",
        "no_data": "No saved data found",
        "load_demo": "📋 Load Demo",
        "create_first": "👆 Create your first objective!",
        "language": "Language",
        "fact": "Fact",
        "actual": "Actual",
        "result": "Result",
        "results_breakdown": "Results Breakdown",
        "delete": "Delete",
        "edit_manage": "Edit & Manage",
        "no_objectives_yet": "No objectives in this department yet.",
        "enter_dept_name": "Please enter a department name",
        "key_result": "Key Result",
        "no_krs": "No Key Results. Add some below.",
        "delete_krs": "🗑️ Delete Key Results",
        "performance_level": "Performance Level",
        "below": "Below", "meets": "Meets", "good": "Good", "very_good": "Very Good", "exceptional": "Exceptional",
        "view_grid": "Grid",
        "view_full": "Full",
        "all_departments": "All Departments",
        "overview": "Overview",
        "total_objectives": "Total Objectives",
        "average_score": "Average Score",
        "departments": "Departments",
        "view_mode": "View Mode",
        "actions": "Actions",
        "avg": "Avg",
        "toggle_sidebar": "Toggle sidebar",
        "value": "Value",
    },
    "ru": {
        "title": "OKR Трекер",
        "performance_scale": "Шкала Оценки",
        "department": "Департамент",
        "department_name": "Название Департамента",
        "create_department": "➕ Создать Департамент",
        "select_department": "Выберите Департамент",
        "delete_department": "🗑️ Удалить Департамент",
        "no_departments": "Нет департаментов. Создайте сначала!",
        "create_objective": "➕ Создать Цель",
        "objective_name": "Название Цели",
        "objective": "Цель",
        "add_key_results": "Добавить Ключевые Результаты",
        "kr_name": "Название KR",
        "kr_description": "Описание (подсказка)",
        "kr_description_placeholder": "Введите смысл/описание KR...",
        "type": "Тип",
        "higher_better": "↑ Больше лучше",
        "lower_better": "↓ Меньше лучше",
        "unit": "Единица",
        "thresholds": "Пороги",
        "add_kr": "➕ Добавить KR",
        "added_krs": "Добавленные KR",
        "remove": "Удалить",
        "create": "✅ Создать",
        "enter_name_error": "Введите название и добавьте KR",
        "score": "🎯 Оценка",
        "add_kr_to_obj": "➕ Добавить KR",
        "add": "➕ Добавить",
        "delete_objective": "🗑️ Удалить Цель",
        "export_json": "Экспорт",
        "export_excel": "Экспорт Excel",
        "save_data": "Сохранить",
        "load_data": "📂 Загрузить",
        "data_saved": "✅ Сохранено!",
        "data_loaded": "✅ Загружено!",
        "no_data": "Нет данных",
        "load_demo": "📋 Демо",
        "create_first": "👆 Создайте цель!",
        "language": "Язык",
        "fact": "Факт",
        "actual": "Фактический",
        "result": "Результат",
        "results_breakdown": "Разбивка результатов",
        "delete": "Удалить",
        "edit_manage": "Редактировать",
        "no_objectives_yet": "В этом департаменте пока нет целей.",
        "enter_dept_name": "Введите название департамента",
        "key_result": "Ключевой Результат",
        "no_krs": "Нет KR.",
        "delete_krs": "🗑️ Удалить Ключевые Результаты",
        "performance_level": "Уровень Производительности",
        "below": "Ниже", "meets": "Соответствует", "good": "Хорошо", "very_good": "Очень хорошо",
        "exceptional": "Исключительно",
        "view_grid": "Сетка",
        "view_full": "Полный",
        "all_departments": "Все Департаменты",
        "overview": "Обзор",
        "total_objectives": "Всего целей",
        "average_score": "Средняя оценка",
        "departments": "Департаменты",
        "view_mode": "Режим просмотра",
        "actions": "Действия",
        "avg": "Сред",
        "toggle_sidebar": "Скрыть/показать панель",
        "value": "Значение",
    },
    "uz": {
        "title": "OKR Трекер",
        "performance_scale": "Баҳолаш Шкаласи",
        "department": "Департамент",
        "department_name": "Департамент Номи",
        "create_department": "➕ Департамент Яратиш",
        "select_department": "Департамент Танланг",
        "delete_department": "🗑️ Департамент Ўчириш",
        "no_departments": "Департамент йўқ. Аввал яратинг!",
        "create_objective": "➕ Мақсад Яратиш",
        "objective_name": "Мақсад Номи",
        "objective": "Мақсад",
        "add_key_results": "Калит Натижалар Қўшиш",
        "kr_name": "KR Номи",
        "kr_description": "Тавсиф (кўрсатма)",
        "kr_description_placeholder": "KR маъносини киритинг...",
        "type": "Тури",
        "higher_better": "↑",
        "lower_better": "↓",
        "unit": "Бирлик",
        "thresholds": "Чегаралар",
        "add_kr": "➕ KR Қўшиш",
        "added_krs": "Қўшилган KR",
        "remove": "Ўчириш",
        "create": "✅ Яратиш",
        "enter_name_error": "Ном ва KR киритинг",
        "score": "🎯 Баҳо",
        "add_kr_to_obj": "➕ KR Қўшиш",
        "add": "➕ Қўшиш",
        "delete_objective": "🗑️ Ўчириш",
        "export_json": "Экспорт",
        "export_excel": "Excel Экспорт",
        "save_data": "Сақлаш",
        "load_data": "📂 Юклаш",
        "data_saved": "✅ Сақланди!",
        "data_loaded": "✅ Юкланди!",
        "no_data": "Маълумот йўқ",
        "load_demo": "📋 Демо",
        "create_first": "👆 Мақсад яратинг!",
        "language": "Тил",
        "fact": "Факт",
        "actual": "Ҳақиқий",
        "result": "Натижа",
        "results_breakdown": "Натижалар тафсилоти",
        "delete": "Ўчириш",
        "edit_manage": "Таҳрирлаш",
        "no_objectives_yet": "Бу департаментда ҳали мақсадлар йўқ.",
        "enter_dept_name": "Департамент номини киритинг",
        "key_result": "Калит Натижа",
        "no_krs": "KR йўқ.",
        "delete_krs": "🗑️ Калит Натижаларни Ўчириш",
        "performance_level": "Самарадорлик Даражаси",
        "below": "Ёмон", "meets": "Кутилган", "good": "Яхши", "very_good": "Жуда яхши", "exceptional": "Фантастик",
        "view_grid": "Тўр",
        "view_full": "Тўлиқ",
        "all_departments": "Барча Департаментлар",
        "overview": "Умумий кўриниш",
        "total_objectives": "Жами мақсадлар",
        "average_score": "Ўртача баҳо",
        "departments": "Департаментлар",
        "view_mode": "Кўриш режими",
        "actions": "Амаллар",
        "avg": "Ўрт",
        "toggle_sidebar": "Панелни яшириш/кўрсатиш",
        "value": "Қиймат",
    }
}

LEVELS = {
    "below": {"min": 3.00, "max": 4.24, "color": "#d9534f"},
    "meets": {"min": 4.25, "max": 4.49, "color": "#f0ad4e"},
    "good": {"min": 4.50, "max": 4.74, "color": "#5cb85c"},
    "very_good": {"min": 4.75, "max": 4.99, "color": "#28a745"},
    "exceptional": {"min": 5.00, "max": 5.00, "color": "#1e7b34"},
}

THEME = {
    "sidebar_bg": "#f8f9fa",
    "sidebar_border": "#e0e0e0",
    "main_bg": "#ffffff",
    "card_bg": "#ffffff",
    "card_border": "#e8e8e8",
    "card_shadow": "0 2px 4px rgba(0,0,0,0.08)",
    "text_primary": "#2c3e50",
    "text_secondary": "#7f8c8d",
    "accent": "#3498db",
    "header_bg": "#ffffff",
}

DATA_FILE = "okr_data.json"


def t(key: str) -> str:
    lang = st.session_state.get('language', 'en')
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)


def get_level_label(level_key: str) -> str:
    return t(level_key)


def calculate_score(actual: float, metric_type: str, thresholds: dict) -> dict:
    below_th = thresholds['below']
    meets_th = thresholds['meets']
    good_th = thresholds['good']
    very_good_th = thresholds['very_good']
    exceptional_th = thresholds['exceptional']

    if metric_type == "higher_better":
        if actual >= exceptional_th:
            score = 5.00
            level = "exceptional"
        elif actual >= very_good_th:
            ratio = (actual - very_good_th) / max((exceptional_th - very_good_th), 1)
            score = 4.75 + ratio * 0.24
            level = "very_good"
        elif actual >= good_th:
            ratio = (actual - good_th) / max((very_good_th - good_th), 1)
            score = 4.50 + ratio * 0.24
            level = "good"
        elif actual >= meets_th:
            ratio = (actual - meets_th) / max((good_th - meets_th), 1)
            score = 4.25 + ratio * 0.24
            level = "meets"
        elif actual >= below_th:
            ratio = (actual - below_th) / max((meets_th - below_th), 1)
            score = 3.00 + ratio * 1.24
            level = "below"
        else:
            score = 3.00
            level = "below"
    else:
        # Lower is better
        if actual <= exceptional_th:
            score = 5.00
            level = "exceptional"
        elif actual <= very_good_th:
            ratio = 1 - (actual - exceptional_th) / max((very_good_th - exceptional_th), 1)
            score = 4.75 + ratio * 0.24
            level = "very_good"
        elif actual <= good_th:
            ratio = 1 - (actual - very_good_th) / max((good_th - very_good_th), 1)
            score = 4.50 + ratio * 0.24
            level = "good"
        elif actual <= meets_th:
            ratio = 1 - (actual - good_th) / max((meets_th - good_th), 1)
            score = 4.25 + ratio * 0.24
            level = "meets"
        elif actual <= below_th:
            ratio = 1 - (actual - meets_th) / max((below_th - meets_th), 1)
            score = 3.00 + ratio * 1.24
            level = "below"
        else:
            score = 3.00
            level = "below"

    return {"score": round(min(max(score, 3.0), 5.0), 2), "level": level, "level_info": LEVELS[level]}


def get_level_for_score(score: float) -> dict:
    if score >= 5.00:
        return {**LEVELS['exceptional'], "key": "exceptional"}
    elif score >= 4.75:
        return {**LEVELS['very_good'], "key": "very_good"}
    elif score >= 4.50:
        return {**LEVELS['good'], "key": "good"}
    elif score >= 4.25:
        return {**LEVELS['meets'], "key": "meets"}
    else:
        return {**LEVELS['below'], "key": "below"}


def score_to_percentage(score: float) -> float:
    return round(((score - 3.0) / 2.0) * 100, 1)


def create_gauge(score: float, compact: bool = False) -> str:
    """Returns HTML string with ECharts gauge"""
    import random
    percentage = score_to_percentage(score)
    level_info = get_level_for_score(score)
    level_label = get_level_label(level_info['key'])

    # Use unique ID to avoid conflicts when multiple gauges on page
    gauge_id = f"gauge_{random.randint(10000, 99999)}"

    # Compact mode settings
    height = 130 if compact else 240
    font_size = 12 if compact else 16
    label_size = 8 if compact else 10
    pointer_width = 6 if compact else 10
    axis_width = 15 if compact else 24

    html = f'''
    <div id="{gauge_id}" style="width: 100%; height: {height}px;"></div>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <script>
        var chart = echarts.init(document.getElementById('{gauge_id}'));
        var option = {{
            series: [{{
                type: 'gauge',
                min: 3,
                max: 5,
                splitNumber: 4,
                radius: '90%',
                center: ['50%', '60%'],
                startAngle: 180,
                endAngle: 0,
                axisLine: {{
                    lineStyle: {{
                        width: {axis_width},
                        color: [
                            [0.625, '#d9534f'],
                            [0.745, '#f0ad4e'],
                            [0.87, '#5cb85c'],
                            [0.995, '#28a745'],
                            [1, '#1e7b34']
                        ]
                    }}
                }},
                pointer: {{
                    icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
                    length: '60%',
                    width: {pointer_width},
                    offsetCenter: [0, '-10%'],
                    itemStyle: {{
                        color: '#1a1a2e'
                    }}
                }},
                axisTick: {{
                    length: 5,
                    lineStyle: {{
                        color: 'auto',
                        width: 1
                    }}
                }},
                splitLine: {{
                    length: 10,
                    lineStyle: {{
                        color: 'auto',
                        width: 2
                    }}
                }},
                axisLabel: {{
                    color: '#444',
                    fontSize: {label_size},
                    distance: -35,
                    formatter: function (value) {{
                        return value.toFixed(1);
                    }}
                }},
                title: {{
                    show: false
                }},
                detail: {{
                    fontSize: {font_size},
                    offsetCenter: [0, '55%'],
                    valueAnimation: true,
                    formatter: function (value) {{
                        return value.toFixed(2) + '\\n({percentage}%)';
                    }},
                    color: '#2c3e50',
                    fontFamily: 'Arial',
                    fontWeight: 'bold'
                }},
                data: [{{
                    value: {score},
                    name: '{level_label}'
                }}]
            }}]
        }};
        chart.setOption(option);
    </script>
    '''
    return html


def render_sidebar(departments):
    """Render professional left sidebar with navigation and controls"""
    # Calculate overall stats
    total_objectives = sum(len(d.get('objectives', [])) for d in departments)
    all_scores = []
    for dept in departments:
        for obj in dept.get('objectives', []):
            krs = obj.get('key_results', [])
            if krs:
                results = [calculate_score(kr['actual'], kr['metric_type'], kr['thresholds']) for kr in krs]
                avg_score = sum(r['score'] for r in results) / len(results)
                all_scores.append(avg_score)

    avg_overall = round(sum(all_scores) / len(all_scores), 2) if all_scores else 0
    overall_level = get_level_for_score(avg_overall) if all_scores else {"color": THEME['text_secondary']}

    st.markdown(
        f"<h3 style='font-size:14px; color:{THEME['text_secondary']}; text-transform:uppercase; letter-spacing:1px; margin:0 0 12px 0;'>📊 {t('overview')}</h3>",
        unsafe_allow_html=True)

    st.markdown(
        f"<div style='background:white; padding:12px; border-radius:6px; margin-bottom:8px; border:1px solid {THEME['card_border']};'><div style='font-size:28px; font-weight:bold; color:{THEME['accent']};'>{total_objectives}</div><div style='font-size:12px; color:{THEME['text_secondary']};'>{t('total_objectives')}</div></div>",
        unsafe_allow_html=True)

    st.markdown(
        f"<div style='background:white; padding:12px; border-radius:6px; margin-bottom:20px; border:1px solid {THEME['card_border']};'><div style='font-size:28px; font-weight:bold; color:{overall_level['color']};'>{avg_overall}</div><div style='font-size:12px; color:{THEME['text_secondary']};'>{t('average_score')}</div></div>",
        unsafe_allow_html=True)


def render_objective_card(objective, dept_idx, obj_idx, compact=True):
    """Render objective - grid view with compact cards OR full view with original detailed display"""
    krs = objective.get('key_results', [])
    if not krs:
        st.warning(t("no_krs"))
        return

    # Calculate scores
    results = [calculate_score(kr['actual'], kr['metric_type'], kr['thresholds']) for kr in krs]
    avg_score = sum(r['score'] for r in results) / len(results)
    avg_level = get_level_for_score(avg_score)
    avg_pct = score_to_percentage(avg_score)

    if compact:
        # GRID VIEW - Compact card display wrapped in prominent frame
        st.markdown(
            f"<div style='background:{THEME['card_bg']}; border:2px solid {THEME['card_border']}; border-radius:10px; padding:0; margin-bottom:16px; box-shadow:0 4px 8px rgba(0,0,0,0.12);'>",
            unsafe_allow_html=True)
        st.markdown(
            f"<div style='padding:16px; border-bottom:1px solid {THEME['card_border']}; display:flex; justify-content:space-between; align-items:flex-start; gap:12px;'><h3 style='margin:0; font-size:16px; color:{THEME['text_primary']}; font-weight:600; flex:1; word-wrap:break-word; overflow-wrap:break-word; line-height:1.3;'>{objective['name']}</h3><div style='background:{avg_level['color']}; color:white; padding:4px 12px; border-radius:20px; font-size:14px; font-weight:bold; white-space:nowrap; flex-shrink:0;'>{avg_score:.2f}</div></div>",
            unsafe_allow_html=True)
        st.markdown(
            f"<div style='padding:12px 16px;'><div style='margin-bottom:12px;'><span style='display:inline-block; padding:4px 10px; background:{avg_level['color']}20; color:{avg_level['color']}; border-radius:4px; font-size:11px; font-weight:600; text-transform:uppercase;'>{get_level_label(avg_level['key'])} • {avg_pct}%</span><span style='display:inline-block; padding:4px 10px; margin-left:8px; background:{THEME['sidebar_bg']}; color:{THEME['text_secondary']}; border-radius:4px; font-size:11px;'>{len(krs)} KRs</span></div>",
            unsafe_allow_html=True)

        gauge_html = create_gauge(avg_score, compact=True)
        components.html(gauge_html, height=140)

        # Build KR table rows with colors matching full view
        kr_rows = "".join([
            f'<tr style="border-bottom:1px solid {THEME["card_border"]};">'
            f'<td style="padding:8px; font-size:11px; color:{THEME["text_primary"]}; font-weight:bold;">KR{i + 1}</td>'
            f'<td style="padding:8px; font-size:11px; color:{THEME["text_primary"]};" title="{kr.get("description", "") or kr["name"]}"><span style="cursor:help; border-bottom:1px dotted {THEME["text_secondary"]};">{kr["name"][:25]}{"..." if len(kr["name"]) > 25 else ""}</span></td>'
            f'<td style="padding:8px; font-size:11px; text-align:center; background:#D6E4F0; font-weight:bold; color:{THEME["text_primary"]};">{kr["actual"]}{kr["unit"]}</td>'
            f'<td style="padding:8px; font-size:11px; text-align:center; background:{results[i]["level_info"]["color"]}; color:white; font-weight:bold;">{results[i]["score"]:.2f}</td>'
            f'</tr>'
            for i, kr in enumerate(krs)
        ])

        # Add table with header styling matching full view
        st.markdown(f"""
        <div style='background:{THEME['card_bg']}; border:1px solid {THEME['card_border']}; border-radius:8px; padding:12px; margin-top:8px; margin-bottom:16px;'>
            <table style='width:100%; border-collapse:collapse;'>
                <thead>
                    <tr style='background:#4472C4; color:white;'>
                        <th style='padding:8px; font-size:11px; text-align:left; border-radius:4px 0 0 0;'>KR</th>
                        <th style='padding:8px; font-size:11px; text-align:left;'>{t('key_result')}</th>
                        <th style='padding:8px; font-size:11px; text-align:center; background:#5B9BD5; color:white;'>{t('fact')}</th>
                        <th style='padding:8px; font-size:11px; text-align:center; border-radius:0 4px 0 0;'>{t('score').replace('🎯 ', '')}</th>
                    </tr>
                </thead>
                <tbody>{kr_rows}</tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"✏️ {t('edit_manage')}", expanded=False):
            for kr_idx, kr in enumerate(krs):
                col1, col2 = st.columns([3, 1])
                with col1:
                    kr_desc = kr.get('description', '')
                    if kr_desc:
                        st.write(f"**KR{kr_idx + 1}:** {kr['name']}")
                        st.caption(f"ℹ️ {kr_desc}")
                    else:
                        st.write(f"**KR{kr_idx + 1}:** {kr['name']}")
                with col2:
                    new_val = st.number_input(
                        t("value"),
                        value=float(kr['actual']),
                        key=f"edit_d{dept_idx}_o{obj_idx}_kr{kr_idx}",
                        label_visibility="collapsed"
                    )
                    if new_val != kr['actual']:
                        st.session_state.departments[dept_idx]['objectives'][obj_idx]['key_results'][kr_idx][
                            'actual'] = new_val
                        save_data()
                        st.rerun()

            st.markdown("---")
            if st.button(f"🗑️ {t('delete_objective')}", key=f"del_obj_d{dept_idx}_o{obj_idx}", type="secondary"):
                st.session_state.departments[dept_idx]['objectives'] = [
                    o for o in st.session_state.departments[dept_idx]['objectives'] if o['id'] != objective['id']
                ]
                save_data()
                st.rerun()

        # Close the frame containers for compact view
        st.markdown("</div></div>", unsafe_allow_html=True)

    else:
        # FULL VIEW - Original detailed display with all tables and functionality wrapped in frame
        st.markdown(
            f"<div style='background:{THEME['card_bg']}; border:2px solid {THEME['card_border']}; border-radius:10px; padding:16px; margin-bottom:20px; box-shadow:0 4px 8px rgba(0,0,0,0.12);'>",
            unsafe_allow_html=True)
        st.markdown(
            f"<div style='background:#FFC000; padding:8px 12px; border-radius:5px; display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;'><span style='font-weight:bold; font-size:14px;'>📋 {objective['name']}</span><span style='background:{avg_level['color']}; color:white; padding:4px 12px; border-radius:15px; font-weight:bold; font-size:14px;'>{t('avg')}: {avg_score:.2f}</span></div>",
            unsafe_allow_html=True)

        with st.expander(f"{objective['name']}", expanded=False):
            col_table, col_gauge = st.columns([3, 1])

            with col_table:
                # Build DataFrame for editable table
                table_data = []
                for kr_idx, kr in enumerate(krs):
                    result = results[kr_idx]
                    table_data.append({
                        "KR": f"KR{kr_idx + 1}",
                        t("key_result"): kr['name'],
                        t("fact"): kr['actual'],
                        "Score": result['score'],
                    })

                df = pd.DataFrame(table_data)

                edited_df = st.data_editor(
                    df,
                    column_config={
                        "KR": st.column_config.TextColumn("KR", disabled=True, width="small"),
                        t("key_result"): st.column_config.TextColumn(t("key_result"), disabled=True, width="medium"),
                        t("fact"): st.column_config.NumberColumn(t("fact"), min_value=-1000, max_value=10000, step=1,
                                                                 format="%.1f"),
                        "Score": st.column_config.NumberColumn("Score", disabled=True, format="%.2f", width="small"),
                    },
                    hide_index=True,
                    use_container_width=True,
                    key=f"editor_d{dept_idx}_o{obj_idx}_{objective['id']}"
                )

                for i, row in edited_df.iterrows():
                    if i < len(krs):
                        new_actual = row[t("fact")]
                        if new_actual != krs[i]['actual']:
                            st.session_state.departments[dept_idx]['objectives'][obj_idx]['key_results'][i][
                                'actual'] = new_actual
                            save_data()
                            st.rerun()

                # Results breakdown table
                st.markdown(f"#### {t('results_breakdown')}")

                html_table = f"<table style='width:100%; border-collapse:collapse; font-size:11px; margin-top:5px;'><thead><tr style='background:#4472C4; color:white;'><th style='padding:6px; border:1px solid #2F5496; font-size:11px;'>KR</th><th style='padding:6px; border:1px solid #2F5496; font-size:11px;'>{t('key_result')}</th><th style='padding:6px; border:1px solid #2F5496; font-size:11px;'>{t('fact')}</th><th style='padding:6px; border:1px solid #2F5496; background:#d9534f; font-size:10px;'>{get_level_label('below')}<br><small style='font-size:9px;'>3.00</small></th><th style='padding:6px; border:1px solid #2F5496; background:#f0ad4e; color:#000; font-size:10px;'>{get_level_label('meets')}<br><small style='font-size:9px;'>4.25</small></th><th style='padding:6px; border:1px solid #2F5496; background:#5cb85c; font-size:10px;'>{get_level_label('good')}<br><small style='font-size:9px;'>4.50</small></th><th style='padding:6px; border:1px solid #2F5496; background:#28a745; font-size:10px;'>{get_level_label('very_good')}<br><small style='font-size:9px;'>4.75</small></th><th style='padding:6px; border:1px solid #2F5496; background:#1e7b34; font-size:10px;'>{get_level_label('exceptional')}<br><small style='font-size:9px;'>5.00</small></th><th style='padding:6px; border:1px solid #2F5496; font-size:11px;'>{t('result')}</th></tr></thead><tbody>"

                for kr_idx, kr in enumerate(krs):
                    result = results[kr_idx]
                    th = kr['thresholds']
                    level = result['level']

                    cells = {
                        'below': '' if level != 'below' else 'background:#d9534f; color:white; font-weight:bold;',
                        'meets': '' if level != 'meets' else 'background:#f0ad4e; color:#000; font-weight:bold;',
                        'good': '' if level != 'good' else 'background:#5cb85c; color:white; font-weight:bold;',
                        'very_good': '' if level != 'very_good' else 'background:#28a745; color:white; font-weight:bold;',
                        'exceptional': '' if level != 'exceptional' else 'background:#1e7b34; color:white; font-weight:bold;',
                    }

                    if kr['metric_type'] == "higher_better":
                        th_texts = [f"<{th['below']}", f"≥{th['meets']}", f"≥{th['good']}", f"≥{th['very_good']}",
                                    f"≥{th['exceptional']}"]
                    else:
                        th_texts = [f">{th['below']}", f"≤{th['meets']}", f"≤{th['good']}", f"≤{th['very_good']}",
                                    f"≤{th['exceptional']}"]

                    row_bg = '#F8F9FA' if kr_idx % 2 == 0 else '#FFFFFF'
                    kr_desc = kr.get('description', '') or kr['name']
                    # Escape quotes in description for HTML attribute
                    kr_desc_escaped = kr_desc.replace('"', '&quot;').replace("'", "&#39;")

                    html_table += f"<tr style='background:{row_bg};'><td style='padding:5px; border:1px solid #ddd; font-weight:bold; font-size:11px;'>KR{kr_idx + 1}</td><td style='padding:5px; border:1px solid #ddd; text-align:left; font-size:11px;' title=\"{kr_desc_escaped}\"><span style='cursor:help; border-bottom:1px dotted #7f8c8d;'>{kr['name']}</span></td><td style='padding:5px; border:1px solid #ddd; background:#E2EFDA; font-weight:bold; font-size:11px;'>{kr['actual']}{kr['unit']}</td><td style='padding:5px; border:1px solid #ddd; {cells['below']} font-size:11px;'>{th_texts[0]}</td><td style='padding:5px; border:1px solid #ddd; {cells['meets']} font-size:11px;'>{th_texts[1]}</td><td style='padding:5px; border:1px solid #ddd; {cells['good']} font-size:11px;'>{th_texts[2]}</td><td style='padding:5px; border:1px solid #ddd; {cells['very_good']} font-size:11px;'>{th_texts[3]}</td><td style='padding:5px; border:1px solid #ddd; {cells['exceptional']} font-size:11px;'>{th_texts[4]}</td><td style='padding:5px; border:1px solid #ddd; background:{result['level_info']['color']}; color:white; font-weight:bold; font-size:11px;'>{result['score']:.2f}</td></tr>"

                kr_formula = " + ".join([f"KR{i + 1}" for i in range(len(krs))])
                html_table += f"<tr style='background:#FFF2CC; font-weight:bold;'><td colspan='8' style='padding:8px; border:2px solid #BF9000; text-align:right; font-size:11px;'>({kr_formula}) / {len(krs)} =</td><td style='padding:8px; border:2px solid #BF9000; background:{avg_level['color']}; color:white; font-size:14px;'>{avg_score:.2f}</td></tr></tbody></table>"

                table_height = 60 + (len(krs) * 38) + 45
                components.html(html_table, height=table_height, scrolling=False)

                st.markdown(f"#### {t('delete_krs')}")
                del_cols = st.columns(len(krs) + 1)
                for kr_idx, kr in enumerate(krs):
                    with del_cols[kr_idx]:
                        if st.button(f"{t('delete')} KR{kr_idx + 1}", key=f"del_kr_d{dept_idx}_o{obj_idx}_{kr['id']}"):
                            st.session_state.departments[dept_idx]['objectives'][obj_idx]['key_results'] = [k for k in
                                                                                                            krs if
                                                                                                            k['id'] !=
                                                                                                            kr['id']]
                            save_data()
                            st.rerun()

            with col_gauge:
                st.markdown(f"### {t('score')}")
                gauge_html = create_gauge(avg_score)
                components.html(gauge_html, height=260)

                st.markdown(
                    f"<div style='text-align:center; margin-top:8px;'><div style='background:{avg_level['color']}; color:white; padding:10px; border-radius:8px; font-size:16px; font-weight:bold;'>{get_level_label(avg_level['key'])}<br><small style='font-size:14px;'>{avg_score:.2f} ({avg_pct}%)</small></div></div>",
                    unsafe_allow_html=True)

            # Add KR section
            with st.expander(t("add_kr_to_obj")):
                ac1, ac2, ac3 = st.columns([3, 2, 1])
                with ac1:
                    add_name = st.text_input(t("kr_name"), key=f"add_name_d{dept_idx}_o{obj_idx}")
                with ac2:
                    add_type = st.selectbox(t("type"), ["higher_better", "lower_better"],
                                            format_func=lambda x: "↑" if x == "higher_better" else "↓",
                                            key=f"add_type_d{dept_idx}_o{obj_idx}")
                with ac3:
                    add_unit = st.text_input(t("unit"), value="%", key=f"add_unit_d{dept_idx}_o{obj_idx}")

                # Description field for tooltip
                add_description = st.text_area(t("kr_description"), placeholder=t("kr_description_placeholder"),
                                               key=f"add_desc_d{dept_idx}_o{obj_idx}", height=68)

                at1, at2, at3, at4, at5 = st.columns(5)
                with at1:
                    st.markdown(f"<small style='color:#d9534f;'>● 3.00</small>", unsafe_allow_html=True)
                    add_below = st.number_input(t("below"), value=0.0, key=f"add_below_d{dept_idx}_o{obj_idx}")
                with at2:
                    st.markdown(f"<small style='color:#f0ad4e;'>● 4.25</small>", unsafe_allow_html=True)
                    add_meets = st.number_input(t("meets"), value=60.0, key=f"add_meets_d{dept_idx}_o{obj_idx}")
                with at3:
                    st.markdown(f"<small style='color:#5cb85c;'>● 4.50</small>", unsafe_allow_html=True)
                    add_good = st.number_input(t("good"), value=75.0, key=f"add_good_d{dept_idx}_o{obj_idx}")
                with at4:
                    st.markdown(f"<small style='color:#28a745;'>● 4.75</small>", unsafe_allow_html=True)
                    add_very_good = st.number_input(t("very_good"), value=90.0,
                                                    key=f"add_very_good_d{dept_idx}_o{obj_idx}")
                with at5:
                    st.markdown(f"<small style='color:#1e7b34;'>● 5.00</small>", unsafe_allow_html=True)
                    add_exc = st.number_input(t("exceptional"), value=100.0, key=f"add_exc_d{dept_idx}_o{obj_idx}")

                if st.button(t("add"), key=f"add_btn_d{dept_idx}_o{obj_idx}"):
                    if add_name.strip():
                        st.session_state.departments[dept_idx]['objectives'][obj_idx]['key_results'].append({
                            "id": str(uuid.uuid4()), "name": add_name.strip(), "metric_type": add_type,
                            "unit": add_unit, "description": add_description.strip(),
                            "thresholds": {"below": add_below, "meets": add_meets, "good": add_good,
                                           "very_good": add_very_good, "exceptional": add_exc},
                            "actual": 0.0
                        })
                        save_data()
                        st.rerun()

            # Delete objective
            if st.button(f"{t('delete_objective')} '{objective['name']}'",
                         key=f"del_obj_d{dept_idx}_{objective['id']}"):
                st.session_state.departments[dept_idx]['objectives'] = [o for o in
                                                                        st.session_state.departments[dept_idx][
                                                                            'objectives'] if o['id'] != objective['id']]
                save_data()
                st.rerun()

        # Close the frame container for full view
        st.markdown("</div>", unsafe_allow_html=True)


def save_data():
    data = {
        "departments": st.session_state.departments,
        "language": st.session_state.get('language', 'en')
    }
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # Migration: convert old flat structure to department structure
            if 'objectives' in data and 'departments' not in data:
                # Old format: migrate to new format
                old_objectives = data.get('objectives', [])
                if old_objectives:
                    # Create a default department with all existing objectives
                    departments = [{
                        "id": str(uuid.uuid4()),
                        "name": "Default Department",
                        "objectives": old_objectives
                    }]
                else:
                    departments = []
                return departments, data.get('language', 'en')
            else:
                # New format
                return data.get('departments', []), data.get('language', 'en')
    return [], 'en'


def export_to_excel(departments):
    """Export OKR data to Excel with color-coded formatting"""
    wb = Workbook()
    ws = wb.active
    ws.title = "OKR Export"

    # Define colors for performance levels
    colors = {
        'below': 'd9534f',
        'meets': 'f0ad4e',
        'good': '5cb85c',
        'very_good': '28a745',
        'exceptional': '1e7b34'
    }

    # Define header style
    header_font = Font(bold=True, color='FFFFFF')
    header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
    header_alignment = Alignment(horizontal='center', vertical='center')

    # Add headers
    headers = [t('department'), t('objective'), t('key_result'), t('actual'), t('unit'), t('below'), t('meets'),
               t('good'),
               t('very_good'), t('exceptional'), t('score').replace('🎯 ', ''), t('performance_level')]
    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment

    # Add data
    row_idx = 2
    for dept in departments:
        dept_name = dept['name']
        for obj in dept.get('objectives', []):
            obj_name = obj['name']
            start_row = row_idx  # Track starting row for this objective
            kr_list = obj.get('key_results', [])

            for kr in kr_list:
                # Calculate score
                result = calculate_score(kr['actual'], kr['metric_type'], kr['thresholds'])

                # Write data (department and objective names only in first row, will be merged later)
                ws.cell(row=row_idx, column=1, value=dept_name if row_idx == start_row else '')
                ws.cell(row=row_idx, column=2, value=obj_name if row_idx == start_row else '')
                ws.cell(row=row_idx, column=3, value=kr['name'])
                ws.cell(row=row_idx, column=4, value=kr['actual'])
                ws.cell(row=row_idx, column=5, value=kr['unit'])
                ws.cell(row=row_idx, column=6, value=kr['thresholds']['below'])
                ws.cell(row=row_idx, column=7, value=kr['thresholds']['meets'])
                ws.cell(row=row_idx, column=8, value=kr['thresholds']['good'])
                ws.cell(row=row_idx, column=9, value=kr['thresholds']['very_good'])
                ws.cell(row=row_idx, column=10, value=kr['thresholds']['exceptional'])
                ws.cell(row=row_idx, column=11, value=result['score'])
                ws.cell(row=row_idx, column=12, value=get_level_label(result['level']))

                # Apply color formatting to performance level cell
                level_cell = ws.cell(row=row_idx, column=12)
                level_cell.fill = PatternFill(start_color=colors[result['level']],
                                              end_color=colors[result['level']],
                                              fill_type='solid')
                level_cell.font = Font(bold=True, color='FFFFFF')
                level_cell.alignment = Alignment(horizontal='center', vertical='center')

                # Apply color formatting to score cell
                score_cell = ws.cell(row=row_idx, column=11)
                score_cell.fill = PatternFill(start_color=colors[result['level']],
                                              end_color=colors[result['level']],
                                              fill_type='solid')
                score_cell.font = Font(bold=True, color='FFFFFF')
                score_cell.alignment = Alignment(horizontal='center', vertical='center')

                row_idx += 1

            # Merge cells if there are multiple KRs
            if len(kr_list) > 1:
                end_row = row_idx - 1
                # Merge department name
                ws.merge_cells(start_row=start_row, start_column=1, end_row=end_row, end_column=1)
                # Merge objective name
                ws.merge_cells(start_row=start_row, start_column=2, end_row=end_row, end_column=2)

            # Apply formatting to department and objective cells
            dept_cell = ws.cell(row=start_row, column=1)
            dept_cell.alignment = Alignment(horizontal='center', vertical='center')
            dept_cell.font = Font(bold=True)

            obj_cell = ws.cell(row=start_row, column=2)
            obj_cell.alignment = Alignment(horizontal='center', vertical='center')
            obj_cell.font = Font(bold=True)

            # Add darker border after each objective (bottom of last row)
            end_row = row_idx - 1
            thick_bottom = Side(style='medium', color='000000')
            for col in range(1, 13):  # Columns A to L
                cell = ws.cell(row=end_row, column=col)
                # Preserve existing borders and add thick bottom
                cell.border = Border(
                    left=cell.border.left if cell.border else None,
                    right=cell.border.right if cell.border else None,
                    top=cell.border.top if cell.border else None,
                    bottom=thick_bottom
                )

    # Adjust column widths
    ws.column_dimensions['A'].width = 25  # Department
    ws.column_dimensions['B'].width = 30  # Objective
    ws.column_dimensions['C'].width = 30  # Key Result
    ws.column_dimensions['D'].width = 10  # Actual
    ws.column_dimensions['E'].width = 8  # Unit
    ws.column_dimensions['F'].width = 10  # Below
    ws.column_dimensions['G'].width = 10  # Meets
    ws.column_dimensions['H'].width = 15  # Good
    ws.column_dimensions['I'].width = 15  # Very Good
    ws.column_dimensions['J'].width = 10  # Exceptional
    ws.column_dimensions['K'].width = 10  # Score
    ws.column_dimensions['L'].width = 20  # Performance Level

    # Save to BytesIO
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output.getvalue()


def inject_global_css():
    """Inject custom CSS for professional enterprise appearance"""
    st.markdown("""
    <style>
    /* Remove default Streamlit padding - reduced top space */
    .main .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Reduce expander header padding */
    .streamlit-expanderHeader {
        padding-top: 0.25rem;
        padding-bottom: 0.25rem;
    }

    /* Custom scrollbar */
    .sidebar-container::-webkit-scrollbar {
        width: 8px;
    }
    .sidebar-container::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    .sidebar-container::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="OKR Tracker", page_icon="🎯", layout="wide")
    inject_global_css()

    # Initialize
    if 'initialized' not in st.session_state:
        loaded_departments, loaded_lang = load_data()
        st.session_state.departments = loaded_departments
        st.session_state.language = loaded_lang
        st.session_state.new_krs = []
        st.session_state.initialized = True

    # Compact Professional Header
    col_header, col_lang = st.columns([5, 1])
    with col_header:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
            <span style="font-size:28px;">🎯</span>
            <h1 style="margin:0; font-size:22px; color:{THEME['text_primary']}; font-weight:600;">
                {t("title")}
            </h1>
        </div>
        """, unsafe_allow_html=True)
    with col_lang:
        lang_options = {"en": "🇬🇧 EN", "ru": "🇷🇺 RU", "uz": "🇺🇿 UZ"}
        selected_lang = st.selectbox("", list(lang_options.keys()),
                                     format_func=lambda x: lang_options[x],
                                     index=list(lang_options.keys()).index(st.session_state.language),
                                     label_visibility="collapsed")
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            save_data()
            st.rerun()

    st.markdown(f"<hr style='margin:5px 0; border:1px solid {THEME['card_border']};'>", unsafe_allow_html=True)

    # ===== SIDEBAR TOGGLE =====
    if 'sidebar_collapsed' not in st.session_state:
        st.session_state.sidebar_collapsed = False

    # Toggle button
    col_toggle, col_spacer = st.columns([0.1, 0.9])
    with col_toggle:
        if st.button("◀" if not st.session_state.sidebar_collapsed else "▶",
                     key="sidebar_toggle",
                     help=t("toggle_sidebar")):
            st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed
            st.rerun()

    # ===== MAIN LAYOUT: SIDEBAR + DASHBOARD =====
    if st.session_state.sidebar_collapsed:
        # Sidebar is hidden, show only main content
        col_main = st.container()
    else:
        # Sidebar is visible, use two-column layout
        col_sidebar, col_main = st.columns([0.22, 0.78], gap="medium")

    if not st.session_state.sidebar_collapsed:
        with col_sidebar:
            # === SIDEBAR ===
            # Sidebar container with background
            st.markdown(f"<style>.main .block-container {{padding-left: 0.5rem; padding-right: 0.5rem;}}</style>",
                        unsafe_allow_html=True)

            # Wrap entire sidebar in a styled container
            st.markdown(
                f"<div style='background:{THEME['sidebar_bg']}; padding:15px; border-radius:8px; border:1px solid {THEME['sidebar_border']};'>",
                unsafe_allow_html=True)

            render_sidebar(st.session_state.departments)

            # Department navigation with dropdown/combo box
            st.markdown(
                f"<h3 style='font-size:14px; color:{THEME['text_secondary']}; text-transform:uppercase; letter-spacing:1px; margin:25px 0 12px 0;'>🏢 {t('departments')}</h3>",
                unsafe_allow_html=True)

            if 'selected_dept_filter' not in st.session_state:
                st.session_state.selected_dept_filter = t("all_departments")

            # Department selectbox/combo box
            if st.session_state.departments:
                dept_options = [t("all_departments")] + [d['name'] for d in st.session_state.departments]
                selected_dept_filter = st.selectbox(
                    t("select_department"),
                    dept_options,
                    index=dept_options.index(
                        st.session_state.selected_dept_filter) if st.session_state.selected_dept_filter in dept_options else 0,
                    label_visibility="collapsed",
                    key="dept_filter_select"
                )
                if selected_dept_filter != st.session_state.selected_dept_filter:
                    st.session_state.selected_dept_filter = selected_dept_filter
                    st.rerun()

            # View mode switcher
            st.markdown(
                f"<h3 style='font-size:14px; color:{THEME['text_secondary']}; text-transform:uppercase; letter-spacing:1px; margin:25px 0 12px 0;'>👁️ {t('view_mode')}</h3>",
                unsafe_allow_html=True)
            view_mode = st.radio(
                "View",
                ["Grid", "Full"],
                horizontal=False,
                label_visibility="collapsed",
                key="view_mode_radio"
            )
            if view_mode.lower() != st.session_state.get('view_mode', 'grid'):
                st.session_state.view_mode = view_mode.lower()

            # Action buttons
            st.markdown(
                f"<h3 style='font-size:14px; color:{THEME['text_secondary']}; text-transform:uppercase; letter-spacing:1px; margin:25px 0 12px 0;'>⚙️ {t('actions')}</h3>",
                unsafe_allow_html=True)

            if st.button("💾 " + t("save_data"), use_container_width=True, type="primary"):
                save_data()
                st.success(t("data_saved"))

            if st.button("📂 " + t("load_data"), use_container_width=True):
                dept, lang = load_data()
                if dept:
                    st.session_state.departments = dept
                    st.session_state.language = lang
                    st.success(t("data_loaded"))
                    st.rerun()
                else:
                    st.warning(t("no_data"))

            # Export buttons
            col_json, col_excel = st.columns(2)
            with col_json:
                if st.button("📄", use_container_width=True, help=t("export_json")):
                    export = []
                    for dept in st.session_state.departments:
                        dept_data = {"department": dept['name'], "objectives": []}
                        for obj in dept.get('objectives', []):
                            obj_data = {"objective": obj['name'], "key_results": []}
                            scores = []
                            for kr in obj['key_results']:
                                res = calculate_score(kr['actual'], kr['metric_type'], kr['thresholds'])
                                scores.append(res['score'])
                                obj_data['key_results'].append({"name": kr['name'], "actual": kr['actual'],
                                                                "score": res['score'], "level": res['level']})
                            obj_data['average'] = round(sum(scores) / len(scores), 2) if scores else 0
                            obj_data['percentage'] = score_to_percentage(obj_data['average'])
                            dept_data['objectives'].append(obj_data)
                        export.append(dept_data)
                    st.json(export)

            with col_excel:
                excel_data = export_to_excel(st.session_state.departments)
                st.download_button(
                    label="📊",
                    data=excel_data,
                    file_name="okr_export.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    help=t("export_excel")
                )

            # Close sidebar container
        st.markdown("</div>", unsafe_allow_html=True)

    with col_main:
        # === MAIN DASHBOARD AREA ===

        # Performance scale legend (compact, always visible)
        st.markdown(f"<p style='font-size:14px; font-weight:600; margin-bottom:8px;'>📊 {t('performance_scale')}</p>",
                    unsafe_allow_html=True)
        cols = st.columns(5)
        for i, key in enumerate(["below", "meets", "good", "very_good", "exceptional"]):
            level = LEVELS[key]
            with cols[i]:
                pct_range = f"{score_to_percentage(level['min'])}%-{score_to_percentage(level['max'])}%"
                st.markdown(
                    f"<div style='background:{level['color']}; color:white; padding:6px 8px; border-radius:4px; text-align:center; font-size:12px;'><b>{get_level_label(key)}</b><br><small style='font-size:10px;'>{level['min']:.2f}-{level['max']:.2f}</small><br><small style='font-size:10px;'>({pct_range})</small></div>",
                    unsafe_allow_html=True)

        st.markdown("---")

        # ===== CREATE DEPARTMENT =====
        with st.expander(t("create_department"), expanded=len(st.session_state.departments) == 0):
            new_dept_name = st.text_input(t("department_name"), key="new_dept_name")
            if st.button(t("create_department") + " ✅", key="create_dept_btn"):
                if new_dept_name.strip():
                    st.session_state.departments.append({
                        "id": str(uuid.uuid4()),
                        "name": new_dept_name.strip(),
                        "objectives": []
                    })
                    save_data()
                    st.rerun()
                else:
                    st.error(t("enter_dept_name"))

        st.markdown("---")

        # ===== CREATE OBJECTIVE =====
        with st.expander(t("create_objective"), expanded=False):
            if not st.session_state.departments:
                st.warning(t("no_departments"))
            else:
                # Department selector
                dept_options = {dept['id']: dept['name'] for dept in st.session_state.departments}
                selected_dept_id = st.selectbox(
                    t("select_department"),
                    options=list(dept_options.keys()),
                    format_func=lambda x: dept_options[x],
                    key="selected_dept_for_obj"
                )

                new_obj_name = st.text_input(t("objective_name"), key="new_obj_name")

                st.markdown(f"#### {t('add_key_results')}")
                c1, c2, c3 = st.columns([3, 2, 1])
                with c1:
                    kr_name = st.text_input(t("kr_name"), key="kr_name_input")
                with c2:
                    kr_type = st.selectbox(t("type"), ["higher_better", "lower_better"],
                                           format_func=lambda x: t("higher_better") if x == "higher_better" else t(
                                               "lower_better"),
                                           key="kr_type_input")
                with c3:
                    kr_unit = st.text_input(t("unit"), value="%", key="kr_unit_input")

                # Description field for tooltip
                kr_description = st.text_area(t("kr_description"), placeholder=t("kr_description_placeholder"),
                                              key="kr_description_input", height=68)

                st.markdown(f"**{t('thresholds')}:**")
                t1, t2, t3, t4, t5 = st.columns(5)
                with t1:
                    st.markdown(f"<small style='color:#d9534f;'>● 3.00</small>", unsafe_allow_html=True)
                    th_below = st.number_input(t("below"), value=0.0, key="th_below")
                with t2:
                    st.markdown(f"<small style='color:#f0ad4e;'>● 4.25</small>", unsafe_allow_html=True)
                    th_meets = st.number_input(t("meets"), value=60.0, key="th_meets")
                with t3:
                    st.markdown(f"<small style='color:#5cb85c;'>● 4.50</small>", unsafe_allow_html=True)
                    th_good = st.number_input(t("good"), value=75.0, key="th_good")
                with t4:
                    st.markdown(f"<small style='color:#28a745;'>● 4.75</small>", unsafe_allow_html=True)
                    th_very_good = st.number_input(t("very_good"), value=90.0, key="th_very_good")
                with t5:
                    st.markdown(f"<small style='color:#1e7b34;'>● 5.00</small>", unsafe_allow_html=True)
                    th_exceptional = st.number_input(t("exceptional"), value=100.0, key="th_exceptional")

                if st.button(t("add_kr")):
                    if kr_name.strip():
                        st.session_state.new_krs.append({
                            "id": str(uuid.uuid4()), "name": kr_name.strip(), "metric_type": kr_type,
                            "unit": kr_unit, "description": kr_description.strip(),
                            "thresholds": {"below": th_below, "meets": th_meets,
                                           "good": th_good, "very_good": th_very_good,
                                           "exceptional": th_exceptional},
                            "actual": 0.0
                        })
                        st.rerun()

                if st.session_state.new_krs:
                    st.markdown(f"**{t('added_krs')}:**")
                    for i, kr in enumerate(st.session_state.new_krs):
                        col1, col2 = st.columns([5, 1])
                        with col1:
                            icon = "↑" if kr['metric_type'] == "higher_better" else "↓"
                            st.write(f"**KR{i + 1}: {kr['name']}** ({icon})")
                        with col2:
                            if st.button(f"❌", key=f"rm_{kr['id']}"):
                                st.session_state.new_krs = [k for k in st.session_state.new_krs if k['id'] != kr['id']]
                                st.rerun()

                if st.button(t("create"), type="primary"):
                    if new_obj_name.strip() and st.session_state.new_krs:
                        # Find the department and add the objective
                        for dept in st.session_state.departments:
                            if dept['id'] == selected_dept_id:
                                dept['objectives'].append({
                                    "id": str(uuid.uuid4()), "name": new_obj_name.strip(),
                                    "key_results": st.session_state.new_krs.copy()
                                })
                                break
                        st.session_state.new_krs = []
                        save_data()
                        st.rerun()
                    else:
                        st.error(t("enter_name_error"))

        st.markdown("---")

        # Display objectives
        if st.session_state.departments:
            view_mode = st.session_state.get('view_mode', 'grid')
            dept_filter = st.session_state.get('selected_dept_filter', t("all_departments"))

            # Filter departments
            if dept_filter == t("all_departments"):
                departments_to_show = st.session_state.departments
            else:
                departments_to_show = [d for d in st.session_state.departments if d['name'] == dept_filter]

            for dept_idx, department in enumerate(st.session_state.departments):
                if dept_filter != t("all_departments") and department['name'] != dept_filter:
                    continue

                # Get actual index in full list
                actual_dept_idx = st.session_state.departments.index(department)

                # Department header
                st.markdown(
                    f"<div style='margin:20px 0 15px 0; padding-bottom:8px; border-bottom:2px solid {THEME['card_border']};'><h2 style='margin:0; font-size:20px; color:{THEME['text_primary']}; font-weight:600;'>📁 {department['name']}</h2></div>",
                    unsafe_allow_html=True)

                objectives = department.get('objectives', [])

                if not objectives:
                    st.info(t("no_objectives_yet"))
                    if st.button(t("delete_department"), key=f"del_dept_{department['id']}", type="secondary"):
                        st.session_state.departments = [d for d in st.session_state.departments if
                                                        d['id'] != department['id']]
                        save_data()
                        st.rerun()
                    continue

                # Render objectives as cards
                if view_mode == 'grid':
                    # Grid layout: 2 columns
                    for row_start in range(0, len(objectives), 2):
                        cols = st.columns(2, gap="medium")
                        for col_idx in range(2):
                            obj_idx = row_start + col_idx
                            if obj_idx < len(objectives):
                                with cols[col_idx]:
                                    render_objective_card(
                                        objectives[obj_idx],
                                        actual_dept_idx,
                                        obj_idx,
                                        compact=True
                                    )
                else:
                    # Full view: single column
                    for obj_idx, objective in enumerate(objectives):
                        render_objective_card(
                            objective,
                            actual_dept_idx,
                            obj_idx,
                            compact=False
                        )

                # Delete department button
                st.markdown("---")
                if st.button(t("delete_department") + f" '{department['name']}'",
                             key=f"del_dept_end_{department['id']}", type="secondary"):
                    st.session_state.departments = [d for d in st.session_state.departments if
                                                    d['id'] != department['id']]
                    save_data()
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    #  Empty state handled in main area
    if not st.session_state.departments:
        with col_main:
            st.info(t("create_first"))
            if st.button(t("load_demo")):
                # Create departments with demo objectives
                st.session_state.departments = [{
                    "id": str(uuid.uuid4()),
                    "name": "PMO - Project Management Office",
                    "objectives": [
                        # Цель 1: Обеспечить своевременную реализацию проектов (20%)
                        {
                            "id": str(uuid.uuid4()),
                            "name": "Цель 1: Обеспечить своевременную реализацию проектов",
                            "weight": 20,
                            "key_results": [
                                {"id": str(uuid.uuid4()),
                                 "name": "KR1.1 Проекты завершенные в срок (% от кол-ва проектов)",
                                 "metric_type": "higher_better", "unit": "%",
                                 "description": "Процент проектов, которые были завершены в установленные сроки. Измеряется как отношение количества проектов, завершенных вовремя, к общему количеству проектов.",
                                 "thresholds": {"below": 50, "meets": 60, "good": 80, "very_good": 100,
                                                "exceptional": 120}, "actual": 0},
                                {"id": str(uuid.uuid4()), "name": "KR1.2 Задачи в JIRA, завершенные в срок (%)",
                                 "metric_type": "higher_better", "unit": "%",
                                 "description": "Процент задач в системе JIRA, выполненных в установленные сроки без переносов дедлайнов.",
                                 "thresholds": {"below": 50, "meets": 65, "good": 95, "very_good": 100,
                                                "exceptional": 200}, "actual": 0},
                                {"id": str(uuid.uuid4()),
                                 "name": "KR1.3 Переносы сроков заверш задач в JIRA (% от общего кол-ва)",
                                 "metric_type": "lower_better", "unit": "%",
                                 "description": "Процент задач, у которых были перенесены сроки выполнения. Чем меньше значение, тем лучше.",
                                 "thresholds": {"below": 30, "meets": 20, "good": 15, "very_good": 5, "exceptional": 0},
                                 "actual": 0},
                            ]
                        },
                        # Цель 2: Управление рисками и бюджетом проектов (20%)
                        {
                            "id": str(uuid.uuid4()),
                            "name": "Цель 2: Управление рисками и бюджетом проектов",
                            "weight": 20,
                            "key_results": [
                                {"id": str(uuid.uuid4()), "name": "KR2.1 Проекты в рамках бюджетов (% без превышения)",
                                 "metric_type": "higher_better", "unit": "%",
                                 "thresholds": {"below": 50, "meets": 60, "good": 75, "very_good": 90,
                                                "exceptional": 100}, "actual": 0},
                                {"id": str(uuid.uuid4()),
                                 "name": "KR2.2 Неучтенные риски возникшие после начала проекта (кол-во)",
                                 "metric_type": "lower_better", "unit": "",
                                 "thresholds": {"below": 10, "meets": 5, "good": 2, "very_good": 1, "exceptional": 0},
                                 "actual": 0},
                                {"id": str(uuid.uuid4()), "name": "KR2.3 Повысить точность оценки трудозатрат до 75%",
                                 "metric_type": "higher_better", "unit": "%",
                                 "thresholds": {"below": 50, "meets": 75, "good": 80, "very_good": 85,
                                                "exceptional": 100}, "actual": 0},
                                {"id": str(uuid.uuid4()), "name": "KR2.4 Процент рисков с планами митигации (%)",
                                 "metric_type": "higher_better", "unit": "%",
                                 "thresholds": {"below": 20, "meets": 50, "good": 60, "very_good": 80,
                                                "exceptional": 100}, "actual": 0},
                            ]
                        },
                        # Цель 3: Управление качеством и отчетность (20%)
                        {
                            "id": str(uuid.uuid4()),
                            "name": "Цель 3: Управление качеством и отчетность",
                            "weight": 20,
                            "key_results": [
                                {"id": str(uuid.uuid4()),
                                 "name": "KR3.1 Своевременность отчетов W,Q,Y, другие (задержка, дней)",
                                 "metric_type": "lower_better", "unit": " дней",
                                 "thresholds": {"below": 5, "meets": 3, "good": 2, "very_good": 1, "exceptional": 0},
                                 "actual": 0},
                                {"id": str(uuid.uuid4()),
                                 "name": "KR3.2 Уровень использования ресурсов (resource utilization) %",
                                 "metric_type": "higher_better", "unit": "%",
                                 "thresholds": {"below": 75, "meets": 85, "good": 90, "very_good": 95,
                                                "exceptional": 100}, "actual": 0},
                                {"id": str(uuid.uuid4()),
                                 "name": "KR3.3 Реагирование на изменения (Response time to changes) часы",
                                 "metric_type": "lower_better", "unit": " часов",
                                 "thresholds": {"below": 5, "meets": 3, "good": 2, "very_good": 1, "exceptional": 0},
                                 "actual": 0},
                                {"id": str(uuid.uuid4()),
                                 "name": "KR3.4 Среднее время от инициации до завершения проекта (нед)",
                                 "metric_type": "lower_better", "unit": " нед",
                                 "thresholds": {"below": 10, "meets": 8, "good": 6, "very_good": 5, "exceptional": 4},
                                 "actual": 0},
                            ]
                        },
                        # Цель 4: Усиление состава и человеческий капитал (10%)
                        {
                            "id": str(uuid.uuid4()),
                            "name": "Цель 4: Усиление состава и человеческий капитал",
                            "weight": 10,
                            "key_results": [
                                {"id": str(uuid.uuid4()),
                                 "name": "KR4.1 Комплектация штата (6 свободных вакансий в штате)",
                                 "metric_type": "higher_better", "unit": "",
                                 "thresholds": {"below": 2, "meets": 3, "good": 4, "very_good": 5, "exceptional": 6},
                                 "actual": 0},
                                {"id": str(uuid.uuid4()), "name": "KR4.2 Набор и подготовка стажеров (16 вакансий)",
                                 "metric_type": "higher_better", "unit": "",
                                 "thresholds": {"below": 3, "meets": 6, "good": 10, "very_good": 12, "exceptional": 16},
                                 "actual": 0},
                                {"id": str(uuid.uuid4()), "name": "KR4.3 % сотрудников с ростом оклада, должности",
                                 "metric_type": "higher_better", "unit": "%",
                                 "thresholds": {"below": 0, "meets": 10, "good": 20, "very_good": 30,
                                                "exceptional": 40}, "actual": 0},
                            ]
                        },
                        # Цель 5: Улучшение продуктов (10%)
                        {
                            "id": str(uuid.uuid4()),
                            "name": "Цель 5: Улучшение продуктов",
                            "weight": 10,
                            "key_results": [
                                {"id": str(uuid.uuid4()),
                                 "name": "KR5.1 Увеличить долю проектов, связанных со стратегическими целями Банка, до 85%",
                                 "metric_type": "higher_better", "unit": "%",
                                 "thresholds": {"below": 75, "meets": 85, "good": 90, "very_good": 95,
                                                "exceptional": 100}, "actual": 0},
                                {"id": str(uuid.uuid4()),
                                 "name": "KR5.2 % продуктов с повторными багами (Defect/error rate)",
                                 "metric_type": "lower_better", "unit": "%",
                                 "thresholds": {"below": 20, "meets": 15, "good": 10, "very_good": 5, "exceptional": 0},
                                 "actual": 0},
                                {"id": str(uuid.uuid4()),
                                 "name": "KR5.3 Обеспечить участие 100% членов команды в обучении по Agile/Scrum",
                                 "metric_type": "higher_better", "unit": "%",
                                 "thresholds": {"below": 80, "meets": 90, "good": 95, "very_good": 100,
                                                "exceptional": 100}, "actual": 0},
                                {"id": str(uuid.uuid4()),
                                 "name": "KR5.4 Провести 6 внутренних воркшопов по методологиям и новым технологиям",
                                 "metric_type": "higher_better", "unit": "",
                                 "thresholds": {"below": 4, "meets": 6, "good": 7, "very_good": 8, "exceptional": 9},
                                 "actual": 0},
                            ]
                        },
                        # Цель 6: Системная и бизнес аналитика и ее автоматизация (20%)
                        {
                            "id": str(uuid.uuid4()),
                            "name": "Цель 6: Системная и бизнес аналитика и ее автоматизация",
                            "weight": 20,
                            "key_results": [
                                {"id": str(uuid.uuid4()),
                                 "name": "KR6.1 Уровень автоматизации процессов проектного управления",
                                 "metric_type": "higher_better", "unit": "%",
                                 "thresholds": {"below": 75, "meets": 85, "good": 90, "very_good": 95,
                                                "exceptional": 100}, "actual": 0},
                                {"id": str(uuid.uuid4()),
                                 "name": "KR6.2 Качество описание бизнес процессов (изменение BPMN) %",
                                 "metric_type": "lower_better", "unit": "%",
                                 "thresholds": {"below": 20, "meets": 15, "good": 10, "very_good": 5, "exceptional": 0},
                                 "actual": 0},
                                {"id": str(uuid.uuid4()),
                                 "name": "KR6.3 Процент изменений плана проекта после планирования",
                                 "metric_type": "lower_better", "unit": "%",
                                 "thresholds": {"below": 20, "meets": 15, "good": 10, "very_good": 5, "exceptional": 0},
                                 "actual": 0},
                            ]
                        },
                    ]
                }]
                save_data()
                st.rerun()


if __name__ == "__main__":
    main()