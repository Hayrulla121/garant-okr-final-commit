import streamlit as st
import streamlit.components.v1 as components
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
        "qualitative": "📊 Qualitative (A/B/C/D/E)",
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
        "weight": "Weight",
        "objective_weight": "Objective Weight (%)",
        "kr_weight": "KR Weight (%)",
        "weights_warning": "⚠️ Weights should sum to 100%",
        "weights_total": "Total",
        "qualitative_grade": "Grade",
        "grade_a": "A - Exceptional",
        "grade_b": "B - Very Good",
        "grade_c": "C - Good",
        "grade_d": "D - Meets",
        "grade_e": "E - Below",
        "weighted_score": "Weighted Score",
        "dept_weighted_avg": "Dept. Weighted Average",
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
        "qualitative": "📊 Качественный (A/B/C/D/E)",
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
        "weight": "Вес",
        "objective_weight": "Вес цели (%)",
        "kr_weight": "Вес KR (%)",
        "weights_warning": "⚠️ Веса должны составлять 100%",
        "weights_total": "Итого",
        "qualitative_grade": "Оценка",
        "grade_a": "A - Исключительно",
        "grade_b": "B - Очень хорошо",
        "grade_c": "C - Хорошо",
        "grade_d": "D - Соответствует",
        "grade_e": "E - Ниже",
        "weighted_score": "Взвешенная оценка",
        "dept_weighted_avg": "Взвеш. среднее отдела",
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
        "qualitative": "📊 Сифат (A/B/C/D/E)",
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
        "weight": "Вазн",
        "objective_weight": "Мақсад вазни (%)",
        "kr_weight": "KR вазни (%)",
        "weights_warning": "⚠️ Вазнлар 100% бўлиши керак",
        "weights_total": "Жами",
        "qualitative_grade": "Баҳо",
        "grade_a": "A - Фантастик",
        "grade_b": "B - Жуда яхши",
        "grade_c": "C - Яхши",
        "grade_d": "D - Кутилган",
        "grade_e": "E - Ёмон",
        "weighted_score": "Вазнли баҳо",
        "dept_weighted_avg": "Бўлим вазнли ўртача",
    }
}

LEVELS = {
    "below": {"min": 3.00, "max": 4.24, "color": "#d9534f"},
    "meets": {"min": 4.25, "max": 4.49, "color": "#f0ad4e"},
    "good": {"min": 4.50, "max": 4.74, "color": "#5cb85c"},
    "very_good": {"min": 4.75, "max": 4.99, "color": "#28a745"},
    "exceptional": {"min": 5.00, "max": 5.00, "color": "#1e7b34"},
}

# Qualitative grades mapping (A/B/C/D/E to scores)
QUALITATIVE_GRADES = {
    "A": {"score": 5.00, "level": "exceptional"},
    "B": {"score": 4.75, "level": "very_good"},
    "C": {"score": 4.50, "level": "good"},
    "D": {"score": 4.25, "level": "meets"},
    "E": {"score": 3.00, "level": "below"},
}

THEME = {
    "sidebar_bg": "#f5f7fa",
    "sidebar_border": "#e1e5eb",
    "main_bg": "#ffffff",
    "card_bg": "#ffffff",
    "card_border": "#e4e7ec",
    "card_shadow": "0 4px 12px rgba(0,0,0,0.08)",
    "text_primary": "#1a202c",
    "text_secondary": "#64748b",
    "accent": "#0066cc",
    "accent_light": "#e6f0ff",
    "header_bg": "linear-gradient(135deg, #1a365d 0%, #2c5282 100%)",
    "success": "#059669",
    "warning": "#d97706",
    "danger": "#dc2626",
}

DATA_FILE = "okr_data.json"


def t(key: str) -> str:
    lang = st.session_state.get('language', 'en')
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)


def get_level_label(level_key: str) -> str:
    return t(level_key)


def calculate_score(actual, metric_type: str, thresholds: dict) -> dict:
    """Calculate score for a KR. Handles quantitative (higher/lower better) and qualitative (A/B/C/D/E) metrics."""

    # Handle qualitative metrics (A/B/C/D/E grades)
    if metric_type == "qualitative":
        grade = str(actual).upper() if actual else "E"
        if grade in QUALITATIVE_GRADES:
            grade_info = QUALITATIVE_GRADES[grade]
            return {
                "score": grade_info["score"],
                "level": grade_info["level"],
                "level_info": LEVELS[grade_info["level"]],
                "grade": grade
            }
        else:
            # Default to E if invalid grade
            return {
                "score": 3.00,
                "level": "below",
                "level_info": LEVELS["below"],
                "grade": "E"
            }

    # Handle quantitative metrics
    actual = float(actual) if actual else 0.0
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


def calculate_weighted_objective_score(objective: dict) -> dict:
    """Calculate simple average score for an objective."""
    krs = objective.get('key_results', [])
    if not krs:
        return {"score": 0, "level": get_level_for_score(0)}

    results = []
    for kr in krs:
        result = calculate_score(kr['actual'], kr['metric_type'], kr.get('thresholds', {}))
        results.append(result)

    # Calculate simple average
    avg_score = sum(r['score'] for r in results) / len(results) if results else 0

    return {
        "score": round(avg_score, 2),
        "level": get_level_for_score(avg_score),
        "results": results
    }


def calculate_weighted_department_score(department: dict) -> dict:
    """Calculate weighted average score for a department based on objective weights."""
    objectives = department.get('objectives', [])
    if not objectives:
        return {"score": 0, "level": get_level_for_score(0)}

    total_weight = 0
    weighted_sum = 0
    obj_scores = []

    for obj in objectives:
        obj_weight = obj.get('weight') or (100 / len(objectives))  # Default to equal weight, handles None
        obj_result = calculate_weighted_objective_score(obj)
        obj_scores.append(obj_result)
        weighted_sum += obj_result['score'] * obj_weight
        total_weight += obj_weight

    # Calculate weighted average (normalize if weights don't sum to 100)
    if total_weight > 0:
        avg_score = weighted_sum / total_weight
    else:
        avg_score = sum(s['score'] for s in obj_scores) / len(obj_scores) if obj_scores else 0

    return {
        "score": round(avg_score, 2),
        "level": get_level_for_score(avg_score),
        "objective_scores": obj_scores,
        "total_weight": total_weight
    }


def create_gauge(score: float, compact: bool = False) -> str:
    """Returns HTML string with ECharts gauge"""
    import random
    percentage = score_to_percentage(score)
    level_info = get_level_for_score(score)
    level_label = get_level_label(level_info['key'])

    # Use unique ID to avoid conflicts when multiple gauges on page
    gauge_id = f"gauge_{random.randint(10000, 99999)}"

    # Compact mode settings
    height = 180 if compact else 240
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
    # Calculate overall stats using weighted calculations
    total_objectives = sum(len(d.get('objectives', [])) for d in departments)
    dept_scores = []

    for dept in departments:
        if dept.get('objectives'):
            dept_result = calculate_weighted_department_score(dept)
            dept_scores.append(dept_result['score'])

    avg_overall = round(sum(dept_scores) / len(dept_scores), 2) if dept_scores else 0
    overall_level = get_level_for_score(avg_overall) if dept_scores else {"color": THEME['text_secondary']}

    st.markdown(
        f"<h3 style='font-size:11px; color:{THEME['text_secondary']}; text-transform:uppercase; letter-spacing:1.5px; margin:0 0 16px 0; font-weight:600;'>📊 {t('overview')}</h3>",
        unsafe_allow_html=True)

    # Stats cards with gradient backgrounds
    st.markdown(f"""
        <div style='background:linear-gradient(135deg, #e6f0ff 0%, #f0f7ff 100%); padding:16px; border-radius:10px; margin-bottom:12px; border:1px solid #cce0ff;'>
            <div style='font-size:32px; font-weight:700; color:#0066cc; line-height:1;'>{total_objectives}</div>
            <div style='font-size:11px; color:#4a90d9; font-weight:500; text-transform:uppercase; letter-spacing:0.5px; margin-top:4px;'>{t('total_objectives')}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style='background:linear-gradient(135deg, {overall_level['color']}15 0%, {overall_level['color']}08 100%); padding:16px; border-radius:10px; margin-bottom:20px; border:1px solid {overall_level['color']}30;'>
            <div style='font-size:32px; font-weight:700; color:{overall_level['color']}; line-height:1;'>{avg_overall}</div>
            <div style='font-size:11px; color:{overall_level['color']}; font-weight:500; text-transform:uppercase; letter-spacing:0.5px; margin-top:4px;'>{t('weighted_score')}</div>
        </div>
    """, unsafe_allow_html=True)


def render_objective_card(objective, dept_idx, obj_idx, compact=True):
    """Render objective - grid view with compact cards OR full view with original detailed display"""
    krs = objective.get('key_results', [])
    if not krs:
        st.warning(t("no_krs"))
        return

    # Calculate weighted scores
    obj_result = calculate_weighted_objective_score(objective)
    avg_score = obj_result['score']
    results = obj_result['results']
    avg_level = get_level_for_score(avg_score)
    avg_pct = score_to_percentage(avg_score)
    obj_weight = objective.get('weight') or 0  # Objective weight within department (handles None)

    if compact:
        # GRID VIEW - Professional compact card with modern styling
        # Only include weight badge HTML if weight is set
        if obj_weight > 0:
            weight_badge_html = f"<span style='display:inline-block; padding:5px 12px; background:#fef3c7; color:#d97706; border-radius:6px; font-size:11px; font-weight:600;'>{t('weight')}: {obj_weight}%</span>"
        else:
            weight_badge_html = ""

        # Use Streamlit container with border for the card
        with st.container(border=True):
            # Header section
            st.markdown(f"""
                <div style='background:linear-gradient(180deg, {avg_level['color']}08 0%, #ffffff 100%); padding:16px; margin-bottom:16px; border-bottom:3px solid {avg_level['color']}; border-radius:8px 8px 0 0;'>
                    <div style='display:flex; justify-content:space-between; align-items:flex-start; gap:12px;'>
                        <h3 style='margin:0; font-size:16px; color:{THEME['text_primary']}; font-weight:700; flex:1; word-wrap:break-word; overflow-wrap:break-word; line-height:1.4;'>📋 {objective['name']}</h3>
                        <div style='background:linear-gradient(135deg, {avg_level['color']} 0%, {avg_level['color']}dd 100%); color:white; padding:8px 16px; border-radius:20px; font-size:15px; font-weight:700; white-space:nowrap; flex-shrink:0; box-shadow:0 3px 10px {avg_level['color']}50;'>{avg_score:.2f}</div>
                    </div>
                    <div style='margin-top:14px; display:flex; gap:10px; flex-wrap:wrap;'>
                        <span style='display:inline-block; padding:6px 14px; background:{avg_level['color']}15; color:{avg_level['color']}; border:1px solid {avg_level['color']}30; border-radius:8px; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;'>{get_level_label(avg_level['key'])} • {avg_pct}%</span>
                        <span style='display:inline-block; padding:6px 14px; background:#f1f5f9; color:{THEME['text_secondary']}; border:1px solid #e2e8f0; border-radius:8px; font-size:12px; font-weight:600;'>{len(krs)} KRs</span>
                        {weight_badge_html}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            gauge_html = create_gauge(avg_score, compact=False)
            components.html(gauge_html, height=260)

            # Editable table for facts
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

            # Editable table for Fact column
            edited_df = st.data_editor(
                df,
                column_config={
                    "KR": st.column_config.TextColumn("KR", disabled=True, width="small"),
                    t("key_result"): st.column_config.TextColumn(t("key_result"), disabled=True, width="medium"),
                    t("fact"): st.column_config.NumberColumn(t("fact"), min_value=-1000, max_value=10000,
                                                             step=1, format="%.1f"),
                    "Score": st.column_config.NumberColumn("Score", disabled=True, format="%.2f", width="small"),
                },
                hide_index=True,
                use_container_width=True,
                key=f"grid_editor_d{dept_idx}_o{obj_idx}_{objective['id']}"
            )

            # Update actual values from edited dataframe
            for i, row in edited_df.iterrows():
                if i < len(krs):
                    new_actual = row[t("fact")]
                    if new_actual != krs[i]['actual']:
                        st.session_state.departments[dept_idx]['objectives'][obj_idx]['key_results'][i]['actual'] = new_actual
                        save_data()
                        st.rerun()

            with st.expander(f"🗑️ {t('delete_krs')}", expanded=False):
                for kr_idx, kr in enumerate(krs):
                    if st.button(f"{t('delete')} KR{kr_idx + 1}", key=f"del_grid_kr_d{dept_idx}_o{obj_idx}_{kr['id']}"):
                        st.session_state.departments[dept_idx]['objectives'][obj_idx]['key_results'] = [
                            k for k in krs if k['id'] != kr['id']
                        ]
                        save_data()
                        st.rerun()

                if st.button(f"🗑️ {t('delete_objective')}", key=f"del_obj_d{dept_idx}_o{obj_idx}", type="secondary"):
                    st.session_state.departments[dept_idx]['objectives'] = [
                        o for o in st.session_state.departments[dept_idx]['objectives'] if o['id'] != objective['id']
                    ]
                    save_data()
                    st.rerun()

    else:
        # FULL VIEW - Original detailed display with all tables and functionality wrapped in frame
        obj_weight = objective.get('weight') or 0  # handles None values
        weight_badge = f"<span style='background:#fef3c7; color:#d97706; padding:4px 10px; border-radius:12px; font-weight:600; font-size:12px; margin-left:8px;'>{t('weight')}: {obj_weight}%</span>" if obj_weight > 0 else ""

        st.markdown(
            f"<div style='background:{THEME['card_bg']}; border:none; border-radius:10px; padding:0; margin-bottom:20px; box-shadow:0 4px 12px rgba(0,0,0,0.1); overflow:hidden;'>",
            unsafe_allow_html=True)
        st.markdown(
            f"<div style='background:#FFC000; padding:8px 12px; border-radius:5px; display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;'><span style='font-weight:bold; font-size:14px;'>📋 {objective['name']}{weight_badge}</span><span style='background:{avg_level['color']}; color:white; padding:4px 12px; border-radius:15px; font-weight:bold; font-size:14px;'>{t('weighted_score')}: {avg_score:.2f}</span></div>",
            unsafe_allow_html=True)

        with st.expander(f"{objective['name']}", expanded=False):
            col_table, col_gauge = st.columns([3, 1])

            with col_table:
                # Build DataFrame for editable table (KR, Key Result, Fact, Score only)
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

                # Editable table for Fact column
                edited_df = st.data_editor(
                    df,
                    column_config={
                        "KR": st.column_config.TextColumn("KR", disabled=True, width="small"),
                        t("key_result"): st.column_config.TextColumn(t("key_result"), disabled=True,
                                                                     width="medium"),
                        t("fact"): st.column_config.NumberColumn(t("fact"), min_value=-1000, max_value=10000,
                                                                 step=1, format="%.1f"),
                        "Score": st.column_config.NumberColumn("Score", disabled=True, format="%.2f",
                                                               width="small"),
                    },
                    hide_index=True,
                    use_container_width=True,
                    key=f"editor_d{dept_idx}_o{obj_idx}_{objective['id']}"
                )

                # Update actual values from edited dataframe
                for i, row in edited_df.iterrows():
                    if i < len(krs):
                        new_actual = row[t("fact")]
                        if new_actual != krs[i]['actual']:
                            st.session_state.departments[dept_idx]['objectives'][obj_idx]['key_results'][i]['actual'] = new_actual
                            save_data()
                            st.rerun()

                # Results breakdown table (without weights)
                st.markdown(f"#### {t('results_breakdown')}")

                html_table = f"<table style='width:100%; border-collapse:collapse; font-size:11px; margin-top:5px;'><thead><tr style='background:#4472C4; color:white;'><th style='padding:6px; border:1px solid #2F5496; font-size:11px;'>KR</th><th style='padding:6px; border:1px solid #2F5496; font-size:11px;'>{t('key_result')}</th><th style='padding:6px; border:1px solid #2F5496; font-size:11px;'>{t('fact')}</th><th style='padding:6px; border:1px solid #2F5496; background:#d9534f; font-size:10px;'>{get_level_label('below')}<br><small style='font-size:9px;'>3.00</small></th><th style='padding:6px; border:1px solid #2F5496; background:#f0ad4e; color:#000; font-size:10px;'>{get_level_label('meets')}<br><small style='font-size:9px;'>4.25</small></th><th style='padding:6px; border:1px solid #2F5496; background:#5cb85c; font-size:10px;'>{get_level_label('good')}<br><small style='font-size:9px;'>4.50</small></th><th style='padding:6px; border:1px solid #2F5496; background:#28a745; font-size:10px;'>{get_level_label('very_good')}<br><small style='font-size:9px;'>4.75</small></th><th style='padding:6px; border:1px solid #2F5496; background:#1e7b34; font-size:10px;'>{get_level_label('exceptional')}<br><small style='font-size:9px;'>5.00</small></th><th style='padding:6px; border:1px solid #2F5496; font-size:11px;'>{t('result')}</th></tr></thead><tbody>"

                for kr_idx, kr in enumerate(krs):
                    result = results[kr_idx]
                    th = kr.get('thresholds', {})
                    level = result['level']

                    cells = {
                        'below': '' if level != 'below' else 'background:#d9534f; color:white; font-weight:bold;',
                        'meets': '' if level != 'meets' else 'background:#f0ad4e; color:#000; font-weight:bold;',
                        'good': '' if level != 'good' else 'background:#5cb85c; color:white; font-weight:bold;',
                        'very_good': '' if level != 'very_good' else 'background:#28a745; color:white; font-weight:bold;',
                        'exceptional': '' if level != 'exceptional' else 'background:#1e7b34; color:white; font-weight:bold;',
                    }

                    # Handle qualitative vs quantitative display
                    if kr['metric_type'] == 'qualitative':
                        actual_display = kr.get('actual', 'E')
                        th_texts = ["E", "D", "C", "B", "A"]
                    elif kr['metric_type'] == "higher_better":
                        actual_display = f"{kr['actual']}{kr.get('unit', '')}"
                        th_texts = [f"<{th.get('below', 0)}", f"≥{th.get('meets', 0)}", f"≥{th.get('good', 0)}",
                                    f"≥{th.get('very_good', 0)}", f"≥{th.get('exceptional', 0)}"]
                    else:
                        actual_display = f"{kr['actual']}{kr.get('unit', '')}"
                        th_texts = [f">{th.get('below', 0)}", f"≤{th.get('meets', 0)}", f"≤{th.get('good', 0)}",
                                    f"≤{th.get('very_good', 0)}", f"≤{th.get('exceptional', 0)}"]

                    row_bg = '#F8F9FA' if kr_idx % 2 == 0 else '#FFFFFF'
                    kr_desc = kr.get('description', '') or kr['name']
                    kr_desc_escaped = kr_desc.replace('"', '&quot;').replace("'", "&#39;")

                    html_table += f"<tr style='background:{row_bg};'><td style='padding:5px; border:1px solid #ddd; font-weight:bold; font-size:11px;'>KR{kr_idx + 1}</td><td style='padding:5px; border:1px solid #ddd; text-align:left; font-size:11px;' title=\"{kr_desc_escaped}\"><span style='cursor:help; border-bottom:1px dotted #7f8c8d;'>{kr['name']}</span></td><td style='padding:5px; border:1px solid #ddd; background:#E2EFDA; font-weight:bold; font-size:11px;'>{actual_display}</td><td style='padding:5px; border:1px solid #ddd; {cells['below']} font-size:11px;'>{th_texts[0]}</td><td style='padding:5px; border:1px solid #ddd; {cells['meets']} font-size:11px;'>{th_texts[1]}</td><td style='padding:5px; border:1px solid #ddd; {cells['good']} font-size:11px;'>{th_texts[2]}</td><td style='padding:5px; border:1px solid #ddd; {cells['very_good']} font-size:11px;'>{th_texts[3]}</td><td style='padding:5px; border:1px solid #ddd; {cells['exceptional']} font-size:11px;'>{th_texts[4]}</td><td style='padding:5px; border:1px solid #ddd; background:{result['level_info']['color']}; color:white; font-weight:bold; font-size:11px;'>{result['score']:.2f}</td></tr>"

                # Simple average formula display (without weights)
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
    """Export OKR data to Excel with color-coded formatting and qualitative support"""
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
    weight_fill = PatternFill(start_color='d97706', end_color='d97706', fill_type='solid')
    header_alignment = Alignment(horizontal='center', vertical='center')

    # Add headers (without KR weight)
    headers = [t('department'), t('objective'), t('objective_weight'), t('key_result'),
               t('type'), t('actual'), t('unit'), t('below'), t('meets'), t('good'),
               t('very_good'), t('exceptional'), t('score').replace('🎯 ', ''), t('performance_level')]
    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = weight_fill if header == t('objective_weight') else header_fill
        cell.alignment = header_alignment

    # Add data
    row_idx = 2
    for dept in departments:
        dept_name = dept['name']
        dept_start_row = row_idx  # Track starting row for this department

        for obj in dept.get('objectives', []):
            obj_name = obj['name']
            obj_weight = obj.get('weight') or 0  # handles None values
            obj_start_row = row_idx  # Track starting row for this objective
            kr_list = obj.get('key_results', [])

            for kr in kr_list:
                # Calculate score
                result = calculate_score(kr['actual'], kr['metric_type'], kr.get('thresholds', {}))

                # Determine metric type display
                if kr['metric_type'] == 'qualitative':
                    type_display = 'Qualitative (A-E)'
                    actual_display = kr.get('actual', 'E')
                elif kr['metric_type'] == 'higher_better':
                    type_display = '↑ Higher Better'
                    actual_display = kr['actual']
                else:
                    type_display = '↓ Lower Better'
                    actual_display = kr['actual']

                # Write data (department only in first row of dept, objective only in first row of obj)
                ws.cell(row=row_idx, column=1, value=dept_name if row_idx == dept_start_row else '')
                ws.cell(row=row_idx, column=2, value=obj_name if row_idx == obj_start_row else '')
                ws.cell(row=row_idx, column=3, value=f"{obj_weight}%" if row_idx == obj_start_row else '')
                ws.cell(row=row_idx, column=4, value=kr['name'])
                ws.cell(row=row_idx, column=5, value=type_display)
                ws.cell(row=row_idx, column=6, value=actual_display)
                ws.cell(row=row_idx, column=7, value=kr.get('unit', ''))

                # Thresholds (show N/A for qualitative)
                th = kr.get('thresholds', {})
                if kr['metric_type'] == 'qualitative':
                    ws.cell(row=row_idx, column=8, value='E')
                    ws.cell(row=row_idx, column=9, value='D')
                    ws.cell(row=row_idx, column=10, value='C')
                    ws.cell(row=row_idx, column=11, value='B')
                    ws.cell(row=row_idx, column=12, value='A')
                else:
                    ws.cell(row=row_idx, column=8, value=th.get('below', 0))
                    ws.cell(row=row_idx, column=9, value=th.get('meets', 0))
                    ws.cell(row=row_idx, column=10, value=th.get('good', 0))
                    ws.cell(row=row_idx, column=11, value=th.get('very_good', 0))
                    ws.cell(row=row_idx, column=12, value=th.get('exceptional', 0))

                ws.cell(row=row_idx, column=13, value=result['score'])
                ws.cell(row=row_idx, column=14, value=get_level_label(result['level']))

                # Apply color formatting to performance level cell
                level_cell = ws.cell(row=row_idx, column=14)
                level_cell.fill = PatternFill(start_color=colors[result['level']],
                                              end_color=colors[result['level']],
                                              fill_type='solid')
                level_cell.font = Font(bold=True, color='FFFFFF')
                level_cell.alignment = Alignment(horizontal='center', vertical='center')

                # Apply color formatting to score cell
                score_cell = ws.cell(row=row_idx, column=13)
                score_cell.fill = PatternFill(start_color=colors[result['level']],
                                              end_color=colors[result['level']],
                                              fill_type='solid')
                score_cell.font = Font(bold=True, color='FFFFFF')
                score_cell.alignment = Alignment(horizontal='center', vertical='center')

                # Apply weight column styling (only objective weight)
                obj_weight_cell = ws.cell(row=row_idx, column=3)
                obj_weight_cell.fill = PatternFill(start_color='fef3c7', end_color='fef3c7', fill_type='solid')
                obj_weight_cell.font = Font(bold=True, color='d97706')

                row_idx += 1

            # Merge objective cells if there are multiple KRs
            if len(kr_list) > 1:
                obj_end_row = row_idx - 1
                # Merge objective name
                ws.merge_cells(start_row=obj_start_row, start_column=2, end_row=obj_end_row, end_column=2)
                # Merge objective weight
                ws.merge_cells(start_row=obj_start_row, start_column=3, end_row=obj_end_row, end_column=3)

            # Apply formatting to objective cell
            obj_cell = ws.cell(row=obj_start_row, column=2)
            obj_cell.alignment = Alignment(horizontal='center', vertical='center')
            obj_cell.font = Font(bold=True)

            # Add darker border after each objective (bottom of last row)
            obj_end_row = row_idx - 1
            thick_bottom = Side(style='medium', color='000000')
            for col in range(1, 15):
                cell = ws.cell(row=obj_end_row, column=col)
                cell.border = Border(
                    left=cell.border.left if cell.border else None,
                    right=cell.border.right if cell.border else None,
                    top=cell.border.top if cell.border else None,
                    bottom=thick_bottom
                )

        # Merge department cells across ALL objectives in this department
        dept_end_row = row_idx - 1
        if dept_end_row > dept_start_row:
            ws.merge_cells(start_row=dept_start_row, start_column=1, end_row=dept_end_row, end_column=1)

        # Apply formatting to department cell
        dept_cell = ws.cell(row=dept_start_row, column=1)
        dept_cell.alignment = Alignment(horizontal='center', vertical='center')
        dept_cell.font = Font(bold=True)

    ws.column_dimensions['A'].width = 20  # Department
    ws.column_dimensions['B'].width = 30  # Objective
    ws.column_dimensions['C'].width = 12  # Objective Weight
    ws.column_dimensions['D'].width = 35  # Key Result
    ws.column_dimensions['E'].width = 15  # Type
    ws.column_dimensions['F'].width = 10  # Actual
    ws.column_dimensions['G'].width = 8  # Unit
    ws.column_dimensions['H'].width = 10  # Below
    ws.column_dimensions['I'].width = 10  # Meets
    ws.column_dimensions['J'].width = 10  # Good
    ws.column_dimensions['K'].width = 12  # Very Good
    ws.column_dimensions['L'].width = 12  # Exceptional
    ws.column_dimensions['M'].width = 10  # Score
    ws.column_dimensions['N'].width = 18  # Performance Level

    # Save to BytesIO
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output.getvalue()


def inject_global_css():
    """Inject custom CSS for professional enterprise appearance"""
    st.markdown("""
    <style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global font and background */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .main {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }
    ß

    /* ===== AGGRESSIVE TOP SPACE REMOVAL ===== */
    /* Remove default Streamlit padding */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        max-width: 100%;
    }

    /* Target the root app container */
    .stApp {
        margin-top: -80px !important;
    }

    /* Alternative: use negative margin on main content */
    [data-testid="stAppViewContainer"] {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    [data-testid="stAppViewContainer"] > .main {
        padding-top: 0 !important;
    }

    /* Hide Streamlit branding and COMPLETELY remove header space */
    #MainMenu {display: none !important;}
    footer {display: none !important;}
    header {display: none !important; height: 0 !important;}

    /* Remove header element completely */
    [data-testid="stHeader"] {
        display: none !important;
        height: 0 !important;
    }

    .stApp > header {
        display: none !important;
        height: 0 !important;
    }

    /* Remove any top decoration/toolbar */
    [data-testid="stToolbar"] {
        display: none !important;
    }

    /* Remove deploy button area */
    [data-testid="stDecoration"] {
        display: none !important;
    }

    /* Remove top bar/status bar */
    [data-testid="stStatusWidget"] {
        display: none !important;
    }

    /* Ensure no top margin on first element */
    .element-container:first-child {
        margin-top: 0 !important;
    }

    /* Target iframe container if embedded */
    .stApp iframe {
        margin-top: 0 !important;
    }
    /* ===== END TOP SPACE REMOVAL ===== */

    /* Professional buttons */
    .stButton>button {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        border-radius: 8px;
        border: 1px solid #e4e7ec;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }

    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
        border: none;
        color: white;
    }

    /* Download button styling */
    .stDownloadButton>button {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        border-radius: 8px;
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        border: none;
        color: white;
        transition: all 0.2s ease;
    }

    .stDownloadButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.4);
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        background: #f8fafc;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        border: 1px solid #e4e7ec;
    }

    .streamlit-expanderContent {
        border: 1px solid #e4e7ec;
        border-top: none;
        border-radius: 0 0 8px 8px;
        background: white;
    }

    /* Input fields */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div {
        font-family: 'Inter', sans-serif;
        border-radius: 8px;
        border: 1px solid #e4e7ec;
    }

    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #0066cc;
        box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
    }

    /* Radio buttons */
    .stRadio>div {
        background: white;
        padding: 0.5rem;
        border-radius: 8px;
        border: 1px solid #e4e7ec;
    }

    /* Metrics and stats cards */
    [data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }

    /* Divider styling */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e4e7ec, transparent);
        margin: 1rem 0;
    }

    /* ===== STICKY SIDEBAR ===== */
    /* Make the sidebar column sticky */
    [data-testid="stHorizontalBlock"] > div:first-child {
        position: sticky;
        top: 0;
        align-self: flex-start;
        max-height: 100vh;
        overflow-y: auto;
    }

    /* Ensure proper scrolling behavior */
    [data-testid="stHorizontalBlock"] {
        align-items: flex-start !important;
    }
    /* ===== END STICKY SIDEBAR ===== */

    /* Alert/warning styling */
    .stAlert {
        border-radius: 8px;
        border: none;
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

    # Top spacing and language selector
    # st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    col_spacer_top, col_lang = st.columns([5, 1])
    with col_lang:
        lang_options = {"en": "🇬🇧 EN", "ru": "🇷🇺 RU", "uz": "🇺🇿 UZ"}
        selected_lang = st.selectbox("Language", list(lang_options.keys()),
                                     format_func=lambda x: lang_options[x],
                                     index=list(lang_options.keys()).index(st.session_state.language),
                                     label_visibility="collapsed")
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            save_data()
            st.rerun()

    # ===== SIDEBAR TOGGLE =====
    if 'sidebar_collapsed' not in st.session_state:
        st.session_state.sidebar_collapsed = False

    # Toggle button
    col_toggle, col_spacer = st.columns([0.1, 0.9])
    with col_toggle:
        if st.button("◀" if not st.session_state.sidebar_collapsed else "▶",
                     key="sidebar_toggle"):
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
                f"<h3 style='font-size:14px; color:{THEME['text_secondary']}; text-transform:uppercase; letter-spacing:1px; margin:25px 0 12px 0;'> {t('view_mode')}</h3>",
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

            # Export button - Excel only
            excel_data = export_to_excel(st.session_state.departments)
            st.download_button(
                label="📊 " + t("export_excel"),
                data=excel_data,
                file_name="okr_export.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

            # Close sidebar container
        st.markdown("</div>", unsafe_allow_html=True)

    with col_main:
        # === MAIN DASHBOARD AREA ===

        # Performance scale legend (simple title + colored boxes, no container)
        st.markdown(f"""
            <p style='font-size:12px; font-weight:600; margin:0 0 12px 0; color:{THEME['text_secondary']}; text-transform:uppercase; letter-spacing:1px;'>📊 {t('performance_scale')}</p>
        """, unsafe_allow_html=True)

        cols = st.columns(5)
        for i, key in enumerate(["below", "meets", "good", "very_good", "exceptional"]):
            level = LEVELS[key]
            with cols[i]:
                pct_range = f"{score_to_percentage(level['min'])}%-{score_to_percentage(level['max'])}%"
                st.markdown(f"""
                    <div style='background:linear-gradient(135deg, {level['color']} 0%, {level['color']}dd 100%); color:white; padding:12px 10px; border-radius:10px; text-align:center; box-shadow:0 2px 8px {level['color']}30; margin-bottom:16px;'>
                        <div style='font-size:12px; font-weight:700; margin-bottom:4px;'>{get_level_label(key)}</div>
                        <div style='font-size:11px; opacity:0.9;'>{level['min']:.2f} - {level['max']:.2f}</div>
                        <div style='font-size:10px; opacity:0.75; margin-top:2px;'>{pct_range}</div>
                    </div>
                """, unsafe_allow_html=True)

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

                # Objective name and weight
                obj_col1, obj_col2 = st.columns([4, 1])
                with obj_col1:
                    new_obj_name = st.text_input(t("objective_name"), key="new_obj_name")
                with obj_col2:
                    new_obj_weight = st.number_input(t("objective_weight"), min_value=0, max_value=100, value=0,
                                                     key="new_obj_weight",
                                                     help="Weight of this objective within department (0-100%)")

                st.markdown(f"#### {t('add_key_results')}")

                # KR basic info (without weight)
                c1, c2, c3 = st.columns([3, 1.5, 1])
                with c1:
                    kr_name = st.text_input(t("kr_name"), key="kr_name_input")
                with c2:
                    kr_type = st.selectbox(t("type"), ["higher_better", "lower_better", "qualitative"],
                                           format_func=lambda x: t(x),
                                           key="kr_type_input")
                with c3:
                    kr_unit = st.text_input(t("unit"), value="%" if kr_type != "qualitative" else "",
                                            key="kr_unit_input",
                                            disabled=(kr_type == "qualitative"))

                # Description field for tooltip
                kr_description = st.text_area(t("kr_description"), placeholder=t("kr_description_placeholder"),
                                              key="kr_description_input", height=68)

                # Show thresholds only for quantitative metrics
                if kr_type != "qualitative":
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
                else:
                    st.info(
                        "📊 Qualitative KRs use A/B/C/D/E grades: A=5.0 (Exceptional), B=4.75 (Very Good), C=4.50 (Good), D=4.25 (Meets), E=3.0 (Below)")
                    th_below, th_meets, th_good, th_very_good, th_exceptional = 0, 0, 0, 0, 0

                if st.button(t("add_kr")):
                    if kr_name.strip():
                        st.session_state.new_krs.append({
                            "id": str(uuid.uuid4()), "name": kr_name.strip(), "metric_type": kr_type,
                            "unit": "" if kr_type == "qualitative" else kr_unit,
                            "description": kr_description.strip(),
                            "thresholds": {"below": th_below, "meets": th_meets,
                                           "good": th_good, "very_good": th_very_good,
                                           "exceptional": th_exceptional},
                            "actual": "E" if kr_type == "qualitative" else 0.0
                        })
                        st.rerun()

                if st.session_state.new_krs:
                    st.markdown(f"**{t('added_krs')}:**")

                    for i, kr in enumerate(st.session_state.new_krs):
                        col1, col2, col3 = st.columns([4, 1, 1])
                        with col1:
                            if kr['metric_type'] == "qualitative":
                                icon = "📊"
                            else:
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
                                    "weight": new_obj_weight,
                                    "key_results": st.session_state.new_krs.copy()
                                })
                                break
                        st.session_state.new_krs = []
                        save_data()
                        st.rerun()
                    else:
                        st.error(t("enter_name_error"))

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
                                 "metric_type": "higher_better", "unit": "%", "weight": 40,
                                 "description": "Процент проектов, которые были завершены в установленные сроки. Измеряется как отношение количества проектов, завершенных вовремя, к общему количеству проектов.",
                                 "thresholds": {"below": 50, "meets": 60, "good": 80, "very_good": 100,
                                                "exceptional": 120}, "actual": 0},
                                {"id": str(uuid.uuid4()), "name": "KR1.2 Задачи в JIRA, завершенные в срок (%)",
                                 "metric_type": "higher_better", "unit": "%", "weight": 35,
                                 "description": "Процент задач в системе JIRA, выполненных в установленные сроки без переносов дедлайнов.",
                                 "thresholds": {"below": 50, "meets": 65, "good": 95, "very_good": 100,
                                                "exceptional": 200}, "actual": 0},
                                {"id": str(uuid.uuid4()),
                                 "name": "KR1.3 Переносы сроков заверш задач в JIRA (% от общего кол-ва)",
                                 "metric_type": "lower_better", "unit": "%", "weight": 25,
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
                                 "metric_type": "higher_better", "unit": "%", "weight": 30,
                                 "thresholds": {"below": 50, "meets": 60, "good": 75, "very_good": 90,
                                                "exceptional": 100}, "actual": 0},
                                {"id": str(uuid.uuid4()),
                                 "name": "KR2.2 Неучтенные риски возникшие после начала проекта (кол-во)",
                                 "metric_type": "lower_better", "unit": "", "weight": 25,
                                 "thresholds": {"below": 10, "meets": 5, "good": 2, "very_good": 1, "exceptional": 0},
                                 "actual": 0},
                                {"id": str(uuid.uuid4()), "name": "KR2.3 Повысить точность оценки трудозатрат до 75%",
                                 "metric_type": "higher_better", "unit": "%", "weight": 25,
                                 "thresholds": {"below": 50, "meets": 75, "good": 80, "very_good": 85,
                                                "exceptional": 100}, "actual": 0},
                                {"id": str(uuid.uuid4()), "name": "KR2.4 Процент рисков с планами митигации (%)",
                                 "metric_type": "higher_better", "unit": "%", "weight": 20,
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
                                 "metric_type": "lower_better", "unit": " дней", "weight": 25,
                                 "thresholds": {"below": 5, "meets": 3, "good": 2, "very_good": 1, "exceptional": 0},
                                 "actual": 0},
                                {"id": str(uuid.uuid4()),
                                 "name": "KR3.2 Уровень использования ресурсов (resource utilization) %",
                                 "metric_type": "higher_better", "unit": "%", "weight": 25,
                                 "thresholds": {"below": 75, "meets": 85, "good": 90, "very_good": 95,
                                                "exceptional": 100}, "actual": 0},
                                {"id": str(uuid.uuid4()),
                                 "name": "KR3.3 Реагирование на изменения (Response time to changes) часы",
                                 "metric_type": "lower_better", "unit": " часов", "weight": 25,
                                 "thresholds": {"below": 5, "meets": 3, "good": 2, "very_good": 1, "exceptional": 0},
                                 "actual": 0},
                                {"id": str(uuid.uuid4()),
                                 "name": "KR3.4 Среднее время от инициации до завершения проекта (нед)",
                                 "metric_type": "lower_better", "unit": " нед", "weight": 25,
                                 "thresholds": {"below": 10, "meets": 8, "good": 6, "very_good": 5, "exceptional": 4},
                                 "actual": 0},
                            ]
                        },
                        # Цель 4: Усиление состава и человеческий капитал (10%) - includes qualitative KR
                        {
                            "id": str(uuid.uuid4()),
                            "name": "Цель 4: Усиление состава и человеческий капитал",
                            "weight": 10,
                            "key_results": [
                                {"id": str(uuid.uuid4()),
                                 "name": "KR4.1 Комплектация штата (6 свободных вакансий в штате)",
                                 "metric_type": "higher_better", "unit": "", "weight": 35,
                                 "thresholds": {"below": 2, "meets": 3, "good": 4, "very_good": 5, "exceptional": 6},
                                 "actual": 0},
                                {"id": str(uuid.uuid4()), "name": "KR4.2 Набор и подготовка стажеров (16 вакансий)",
                                 "metric_type": "higher_better", "unit": "", "weight": 35,
                                 "thresholds": {"below": 3, "meets": 6, "good": 10, "very_good": 12, "exceptional": 16},
                                 "actual": 0},
                                {"id": str(uuid.uuid4()), "name": "KR4.3 Качество развития сотрудников (оценка)",
                                 "metric_type": "qualitative", "unit": "", "weight": 30,
                                 "description": "Качественная оценка программы развития сотрудников. A=Отлично, B=Очень хорошо, C=Хорошо, D=Удовлетворительно, E=Неудовлетворительно",
                                 "thresholds": {"below": 0, "meets": 0, "good": 0, "very_good": 0, "exceptional": 0},
                                 "actual": "C"},
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
                                 "metric_type": "higher_better", "unit": "%", "weight": 30,
                                 "thresholds": {"below": 75, "meets": 85, "good": 90, "very_good": 95,
                                                "exceptional": 100}, "actual": 0},
                                {"id": str(uuid.uuid4()),
                                 "name": "KR5.2 % продуктов с повторными багами (Defect/error rate)",
                                 "metric_type": "lower_better", "unit": "%", "weight": 30,
                                 "thresholds": {"below": 20, "meets": 15, "good": 10, "very_good": 5, "exceptional": 0},
                                 "actual": 0},
                                {"id": str(uuid.uuid4()),
                                 "name": "KR5.3 Обеспечить участие 100% членов команды в обучении по Agile/Scrum",
                                 "metric_type": "higher_better", "unit": "%", "weight": 20,
                                 "thresholds": {"below": 80, "meets": 90, "good": 95, "very_good": 100,
                                                "exceptional": 100}, "actual": 0},
                                {"id": str(uuid.uuid4()),
                                 "name": "KR5.4 Провести 6 внутренних воркшопов по методологиям и новым технологиям",
                                 "metric_type": "higher_better", "unit": "", "weight": 20,
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
                                 "metric_type": "higher_better", "unit": "%", "weight": 40,
                                 "thresholds": {"below": 75, "meets": 85, "good": 90, "very_good": 95,
                                                "exceptional": 100}, "actual": 0},
                                {"id": str(uuid.uuid4()),
                                 "name": "KR6.2 Качество описание бизнес процессов (изменение BPMN) %",
                                 "metric_type": "lower_better", "unit": "%", "weight": 30,
                                 "thresholds": {"below": 20, "meets": 15, "good": 10, "very_good": 5, "exceptional": 0},
                                 "actual": 0},
                                {"id": str(uuid.uuid4()),
                                 "name": "KR6.3 Процент изменений плана проекта после планирования",
                                 "metric_type": "lower_better", "unit": "%", "weight": 30,
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