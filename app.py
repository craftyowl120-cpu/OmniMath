import streamlit as st
import datetime
from engine import MathEngine

# Initialize Engine
if 'engine' not in st.session_state:
    st.session_state.engine = MathEngine()

engine = st.session_state.engine

st.set_page_config(page_title="OmniMath Assistant", page_icon="📐", layout="wide")

st.title("📐 OmniMath Assistant")
st.markdown("Solve Algebra, Arithmetic, Statistics, Trigonometry, and Geometry with step-by-step breakdowns!")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Calculation Settings")
format_mode = st.sidebar.radio(
    "Select Result Format (Algebra only):",
    ["decimal", "fraction", "expanded"],
    index=0,
    horizontal=True
)

st.sidebar.divider()
st.sidebar.header("📜 Calculation History")
history = engine.get_history()

if history:
    for entry in reversed(history):
        with st.sidebar.expander(f"{entry['timestamp']} - {entry['expression']}"):
            st.write(f"**Result:** {entry['result']}")
            if entry['steps']:
                st.write("**Steps:**")
                for step in entry['steps']:
                    st.write(f"- {step}")
else:
    st.sidebar.info("No recent calculations.")

st.sidebar.divider()
if st.sidebar.button("🗑️ Clear History"):
    engine._history = []
    engine._save_history_to_disk()
    st.rerun()

st.sidebar.divider()
        
# --- NEW: AI TUTOR TOGGLE ---
st.sidebar.header("🤖 AI Tutor Mode")
tutor_enabled = st.sidebar.checkbox("Enable Local AI Tutor (Ollama)", value=False)
if tutor_enabled:
    st.sidebar.info("Ensure Ollama is running with llama3!")

with tab1:
    st.subheader("Algebra & Arithmetic")
    with st.form("algebra_form"):
        problem = st.text_input("Enter your problem (e.png, e.g., x + 5 = 10 or 2 * (3 + 4)):")
        submit_algebra = st.form_submit_button("Solve")
    
    if submit_algebra:
        if problem:
            try:
                result, steps = engine.solve(problem, format_type=format_mode)
                st.success(f"**Result:** {result}")
                st.markdown("### Steps")
                for i, step in enumerate(steps):
                    st.write(f"{i+1}. {step}")
                    
                # --- AI TUTOR EXPLANATION ---
                if tutor_enabled:
                    with st.empty() as tutor_placeholder:
                        explanation_text = ""
                        for token in engine.generate_tutor_explanation(problem, steps):
                            explanation_text += token
                            tutor_placeholder.info(f"**Tutor Says:**\n\n{explanation_text}")

            except Exception as e:
                st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter a problem.")

with tab2:
    st.subheader("Statistics")
    with st.form("stats_form"):
        st.markdown("Enter a dataset separated by commas or spaces (e.g., `10, 2 3, 40`)")
        stats_data = st.text_area("Dataset", placeholder="1, 2, 3, 4, 5", height=100)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            operation = st.selectbox(
                "Operation", 
                ["mean", "median", "mode", "variance", "std_dev"],
                format_func=lambda x: x.replace('_', ' ').title()
            )
        with col2:
            st.write("##") # Alignment spacer
            calculate_stats = st.form_submit_button("Calculate Statistics", use_container_width=True)

    if calculate_stats:
        if stats_data.strip():
            try:
                result, steps = engine.calculate_statistics(stats_data, operation)
                if result is not None:
                    st.success(f"**Result:** {result}")
                    if steps:
                        st.markdown("### Steps")
                        for i, step in enumerate(steps):
                            st.write(f"{i+1}. {step}")
                else:
                    if engine.steps:
                        error_step = [s for s in engine.steps if "Error" in s or "Failure" in s]
                        if error_step:
                            st.error(error_step[-1])
                        else:
                            st.error("An error occurred during calculation.")
                    else:
                        st.error("Error in calculation.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a dataset.")

with tab3:
    st.subheader("Trigonometry")
    
    # Initialize session state for the trig expression if it doesn't exist
    if 'trig_expr' not in st.session_state:
        st.session_state.trig_expr = ""

    # Function buttons for quick input (outside the form to trigger rerun)
    st.markdown("🚀 **Quick Functions**")
    btn_cols = st.columns(5)
    funcs = ["sin(", "cos(", "tan(", "atan(", "asin("]
    for idx, func in enumerate(funcs):
        with btn_cols[idx]:
            if st.button(func, key=f"btn_{func}"):
                st.session_state.trig_expr += func
                st.rerun()

    st.markdown("---")

    # The unified form for trigonometric calculation
    with st.form("trig_form"):
        col_unit, col_input = st.columns([1, 2])
        
        with col_unit:
            unit = st.radio("Angle Unit", ["degrees", "radians"], index=0)
            
        with col_input:
            # The expression input is linked to session state to persist "Quick Function" appends
            st.session_state.trig_expr = st.text_input(
                "Trigonometric Expression", 
                value=st.session_state.trig_expr, 
                placeholder="e.g., sin(30)"
            )
        
        submit_trig = st.form_submit_button("Solve Trigonometry", use_container_width=True, type="primary")

    if submit_trig:
        expression = st.session_state.trig_expr
        if expression.strip():
            try:
                result, steps = engine.solve_trig(expression, unit=unit)
                if result is not None:
                    st.success(f"**Result:** {result}")
                    if steps:
                        st.markdown("### Steps")
                        for i, step in enumerate(steps):
                            st.write(f"{i+1}. {step}")
                else:
                    st.error("Error in calculation. Please check your expression.")
            except Exception as e:
                st.error(f"error: {str(e)}")
        else:
            st.warning("Please enter a trigonometric expression.")

with tab4:
    st.subheader("Geometry")
    
    # 1. Select Dimension (2D or 3D)
    dimension = st.selectbox("Select Dimension", ["2D", "3D"], index=0)
    
    # 2. Define shape and operation maps based on dimension
    if dimension == "2D":
        shapes_2d = {
            "Circle": ["area", "perimeter"],
            "Rectangle": ["area", "perimeter"],
            "Triangle": ["area", "perimeter"],
            "Square": ["area", "perimeter"]
        }
        shape_list = list(shapes_2d.keys())
        operation = st.selectbox("Select Operation", ["area", "perimeter"], index=0, key="geo_op_2d")
    else:
        shapes_3d = {
            "Sphere": ["area", "volume"],
            "Cube": ["area", "volume"]
        }
        shape_list = list(shapes_3d.keys())
        operation = st.selectbox("Select Operation", ["area", "volume"], index=0, key="geo_op_3d")

    # 3. Select Specific Shape
    selected_shape = st.selectbox("Select Shape", shape_list)

    # 4. Dynamic Input Fields based on selected shape
    st.divider()
    st.write("### 📐 Dimensions")
    params = {}
    
    # We use a single form for the execution
    with st.form("geometry_form"):
        if selected_shape == "Circle" or selected_shape == "Sphere":
            radius = st.number_input("Radius", min_value=0.0, value=1.0, step=0.1)
            params["radius"] = radius
            
        elif selected_shape == "Rectangle":
            l = st.number_input("Length", min_value=0.0, value=1.0, step=0.1)
            w = st.number_input("Width", min_value=0.0, value=1.0, step=0.1)
            params["length"] = l
            params["width"] = w
            
        elif selected_shape == "Triangle":
            # For simplicity in this version, we handle area/perimeter via base/height or side
            mode = st.radio("Mode", ["Area (Base/Height)", "Perimeter (Equilateral)"], horizontal=True)
            if mode == "Area (Base/Height)":
                b = st.number_input("Base", min_value=0.0, value=1.0, step=0.1)
                h = st.number_input("Height", min_value=0.0, value=1.0, step=0.1)
                params["base"] = b
                params["height"] = h
            else:
                s = st.number_input("Side Length", min_value=0.0, value=1.0, step=0.1)
                params["side"] = s
                
        elif selected_shape == "Square":
            s = st.number_input("Side Length", min_value=0.0, value=1.0, step=0.1)
            params["side"] = s
            
        elif selected_shape == "Cube":
            s = st.number_input("Side Length", min_value=0.0, value=1.0, step=0.1)
            params["side"] = s

        submit_geo = st.form_submit_button("Calculate Geometry", use_container_width=True, type="primary")

        if submit_geo:
            if params:
                try:
                    # Normalize shape name to match engine (lowercase, no spaces)
                    engine_shape = selected_shape.lower()
                    result, steps = engine.solve_geometry(engine_shape, operation, params)
                    
                    if result is not None:
                        st.success(f"**Result:** {result}")
                        if steps:
                            st.markdown("### Steps")
                            for i, step in enumerate(steps):
                                st.write(f"{i+1}. {step}")
                    else:
                        st.error("Error in calculation. Please check your dimensions.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("Please provide dimensions for the shape.")

with tab5:
    st.header("Unit Converter")
    
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("Select Category", ["Length", "Mass", "Volume"])
    with col2:
        # Get available units for this category from the converter
        available_units = list(engine.converter.conversions[category]["units"].keys())
    
    col3, col4 = st.columns(2)
    with col3:
        from_unit = st.selectbox("From", available_units, index=0)
    with col4:
        to_unit = st.selectbox("To", available_units, index=1 if len(available_units) > 1 else 0)
    
    value = st.number_input("Value to convert", value=1.0, format="%f")
    
    if st.button("Convert", use_container_width=True, type="primary"):
        try:
            result, steps = engine.converter.convert(value, category, from_unit, to_unit)
            st.success(f"**Result:** {result:g} {to_unit}")
            
            with st.expander("Show Calculation Steps"):
                for step in steps:
                    st.write(f"• {step}")
            
            # Record to history manually as it's a different method signature
            engine._save_to_history(f"{value} {from_unit} to {to_unit}", f"{result:g}", category)
            
        except Exception as e:
            st.error(f"Conversion Error: {str(e)}")
