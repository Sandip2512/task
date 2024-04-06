import streamlit as st
from PIL import Image
from scipy import stats

def perform_ab_test(control_visitors, control_conversions, treatment_visitors, treatment_conversions, confidence_level):
    # Calculate conversion rates for control and treatment groups
    control_conversion_rate = control_conversions / control_visitors
    treatment_conversion_rate = treatment_conversions / treatment_visitors
    
    # Calculate z-score
    z_score = stats.norm.ppf(1 - (1 - confidence_level / 100) / 2)
    
    # Calculate standard error for control group
    control_standard_error = (control_conversion_rate * (1 - control_conversion_rate) / control_visitors) ** 0.5
    
    # Calculate standard error for treatment group
    treatment_standard_error = (treatment_conversion_rate * (1 - treatment_conversion_rate) / treatment_visitors) ** 0.5
    
    # Calculate pooled standard error
    pooled_standard_error = ((control_standard_error ** 2) + (treatment_standard_error ** 2)) ** 0.5
    
    # Calculate margin of error
    margin_of_error = z_score * pooled_standard_error
    
    # Calculate the difference in conversion rates between treatment and control groups
    difference = treatment_conversion_rate - control_conversion_rate
    
    # Determine the confidence interval
    confidence_interval = (difference - margin_of_error, difference + margin_of_error)
    
    # Perform hypothesis testing
    if confidence_interval[0] > 0:
        return "Experiment Group is Better"
    elif confidence_interval[1] < 0:
        return "Control Group is Better"
    else:
        return "Indeterminate"

image_experiment = Image.open("1.png")
image_control = Image.open("2.png")
image_int = Image.open("intermediate.png")


# Streamlit app
def main():

    # Set page title and favicon
    st.set_page_config(page_title="A/B Test App", page_icon=":bar_chart:")
    st.markdown("<h1 style='color: #ff6347;'>A/B Test Hypothesis Testing App</h1>", unsafe_allow_html=True)
    
    
    st.sidebar.header("Input Parameters")
    
    control_visitors = st.sidebar.text_input("Control Group Visitors", value="874767")
    control_conversions = st.sidebar.text_input("Control Group Conversions", value="874767")
    treatment_visitors = st.sidebar.text_input("Treatment Group Visitors", value="258231")
    treatment_conversions = st.sidebar.text_input("Treatment Group Conversions", value="258231")
    confidence_level = st.sidebar.select_slider("Confidence Level", options=[90, 95, 99], value=95)
    
    if st.sidebar.button("Run A/B Test"):
        result = perform_ab_test(int(control_visitors), int(control_conversions), int(treatment_visitors), int(treatment_conversions), confidence_level)
        st.write("A/B Test Result:", result)

        if result == "Experiment Group is Better":
            st.image(image_experiment, use_column_width=True)
        elif result == "Control Group is Better":
            st.image(image_control, use_column_width=True)
        else:
            st.image(image_int, use_column_width=True)


if __name__ == "__main__":
    main()