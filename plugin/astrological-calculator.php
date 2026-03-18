<?php
/*
Plugin Name: Astrology Sign Calculator
Description: Renders an astrology sign calculator form using shortcode [astrology_calculator]
Version: 1.0
Author: Mohammad Ammad
*/

// Enqueue styles and scripts
function astrology_calculator_enqueue_scripts() {
    wp_enqueue_style('astrology-calculator-style', plugins_url('dist/output.css', __FILE__));
    wp_enqueue_script('astrology-calculator-script', plugins_url('dist/index.js', __FILE__), array(), '1.0', true);
}
add_action('wp_enqueue_scripts', 'astrology_calculator_enqueue_scripts');

// Function to render the HTML
function astrology_calculator_shortcode() {
    ob_start();
    ?>
     <div class="container p-4 md:mx-auto">
      <div id="main-container">
        <div class="flex justify-center items-center flex-col my-3">
          <h1
            class="text-2xl md:text-4xl font-medium text-gray-800 py-2 text-center"
          >
            Calculate Your Signs...
          </h1>
          <p
            class="text-gray-800 text-[12px] md:text-sm text-center max-w-[90%]"
          >
            Use our handy sign calculators to look up in which constellation a
            particular sign was located at the moment of your birth.
          </p>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-3 gap-5">
          <div
            class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
            style="
              box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
            "
            onclick="showForm(
              'Sun Sign Calculator',
              '<?php echo plugins_url('assets/sun.jpg', __FILE__); ?>',
              'Sun'
            )"
          >
            <img src="<?php echo plugins_url('assets/sun.jpg', __FILE__); ?>" alt="" class="w-14" />
            <h3 class="text-2xl text-gray-900">Sun</h3>
          </div>

          <div
            class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
            style="
              box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
            "
            onclick="showForm(
              'Moon Sign Calculator',
              '<?php echo plugins_url('assets/moon.jpg', __FILE__); ?>',
              'Moon'
            )"
          >
            <img src="<?php echo plugins_url('assets/moon.jpg', __FILE__); ?>" alt="" class="w-14" />
            <h3 class="text-2xl text-gray-900">Moon</h3>
          </div>

          <div
            class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
            style="
              box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
            "
            onclick="showForm(
              'Mercury Sign Calculator',
              '<?php echo plugins_url('assets/mercury.jpg', __FILE__); ?>',
              'Mercury'
            )"
          >
            <img src="<?php echo plugins_url('assets/mercury.jpg', __FILE__); ?>" alt="" class="w-14" />
            <h3 class="text-2xl text-gray-900">Mercury</h3>
          </div>

          <div
            class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
            style="
              box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
            "
            onclick="showForm(
              'Venus Sign Calculator',
              '<?php echo plugins_url('assets/venus.jpg', __FILE__); ?>',
              'Venus'
            )"
          >
            <img src="<?php echo plugins_url('assets/venus.jpg', __FILE__); ?>" alt="" class="w-14" />
            <h3 class="text-2xl text-gray-900">Venus</h3>
          </div>

          <div
            class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
            style="
              box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
            "
            onclick="showForm(
              'Mars Sign Calculator',
              '<?php echo plugins_url('assets/mars.jpg', __FILE__); ?>',
              'Mars'
            )"
          >
            <img src="<?php echo plugins_url('assets/mars.jpg', __FILE__); ?>" alt="" class="w-14" />
            <h3 class="text-2xl text-gray-900">Mars</h3>
          </div>

          <div
            class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
            style="
              box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
            "
            onclick="showForm(
              'Jupiter Sign Calculator',
              '<?php echo plugins_url('assets/jupiter.jpg', __FILE__); ?>',
              'Jupiter'
            )"
          >
            <img src="<?php echo plugins_url('assets/jupiter.jpg', __FILE__); ?>" alt="" class="w-14" />
            <h3 class="text-2xl text-gray-900">Jupiter</h3>
          </div>

          <div
            class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
            style="
              box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
            "
            onclick="showForm(
              'Saturn Sign Calculator',
              '<?php echo plugins_url('assets/saturn.jpg', __FILE__); ?>',
              'Saturn'
            )"
          >
            <img src="<?php echo plugins_url('assets/saturn.jpg', __FILE__); ?>" alt="" class="w-14" />
            <h3 class="text-2xl text-gray-900">Saturn</h3>
          </div>

          <div
            class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
            style="
              box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
            "
            onclick="showForm(
              'Uranus Sign Calculator',
              '<?php echo plugins_url('assets/uranus.jpg', __FILE__); ?>',
              'Uranus'
            )"
          >
            <img src="<?php echo plugins_url('assets/uranus.jpg', __FILE__); ?>" alt="" class="w-14" />
            <h3 class="text-2xl text-gray-900">Uranus</h3>
          </div>

          <div
            class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
            style="
              box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
            "
            onclick="showForm(
              'Neptune Sign Calculator',
              '<?php echo plugins_url('assets/neptune.jpg', __FILE__); ?>',
              'Neptune'
            )"
          >
            <img src="<?php echo plugins_url('assets/neptune.jpg', __FILE__); ?>" alt="" class="w-14" />
            <h3 class="text-2xl text-gray-900">Neptune</h3>
          </div>

          <div
            class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
            style="
              box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
            "
            onclick="showForm(
              'Pluto Sign Calculator',
              '<?php echo plugins_url('assets/pluto.jpg', __FILE__); ?>',
              'Pluto'
            )"
          >
            <img src="<?php echo plugins_url('assets/pluto.jpg', __FILE__); ?>" alt="" class="w-14" />
            <h3 class="text-2xl text-gray-900">Pluto</h3>
          </div>

          <div
            class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
            style="
              box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
            "
            onclick="showForm(
              'Ascendant Sign Calculator',
              '<?php echo plugins_url('assets/asc.jpg', __FILE__); ?>',
              'Ascendant'
            )"
          >
            <img src="<?php echo plugins_url('assets/asc.jpg', __FILE__); ?>" alt="" class="w-14" />
            <h3 class="text-2xl text-gray-900">Ascendant</h3>
          </div>
        </div>
      </div>

      <div id="form-container" class="mx-auto md:mt-14">
        <div class="flex justify-start items-center">
          <img src="" alt="" id="top-image" class="w-7" />
          <h4 id="top-title" class="text-gray-900"></h4>
        </div>
        <div class="flex justify-between items-center">
          <h2 id="heading" class="text-3xl text-gray-900 font-semibold"></h2>
          <button
            id="back-btn"
            class="bg-blue-600 text-white px-2 py-1 rounded-md font-semibold mt-2 cursor-pointer"
            onclick="backHandler()"
            >Back</button>
        </div>
        <p id="paragraph" class="text-gray-900 text-sm"></p>

        <div id="error-container">
          <div
            class="bg-red-500 text-white px-4 py-3 rounded relative mt-4"
            role="alert"
          >
            <strong class="font-bold">Error!</strong>
            <span class="block sm:inline" id="error-message"></span>
          </div>
        </div>

        <div class="my-3">
          <form id="form-action">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
              <div class="mb-4">
                <label
                  for="fname"
                  class="block text-sm font-medium text-gray-700 mb-2"
                >
                  First Name
                </label>
                <input
                  type="text"
                  id="fname"
                  name="fname"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter your first name"
                />
              </div>
              <div class="mb-4">
                <label
                  for="fname"
                  class="block text-sm font-medium text-gray-700 mb-2"
                >
                  City of Birth
                </label>
                <select id="city" name="city" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" required>
                  <option value="">Select a city</option>
                </select>
              </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
              <div class="mb-4">
                <label
                  for="dob"
                  class="block text-sm font-medium text-gray-700 mb-2"
                >
                  Date of Birth
                </label>
                <input
                  type="date"
                  id="dob"
                  name="dob"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div class="mb-4">
                <label
                  for="timeOfBirth"
                  class="block text-sm font-medium text-gray-700 mb-2"
                >
                  Time of Birth
                </label>
                <input
                  type="time"
                  id="timeOfBirth"
                  name="timeOfBirth"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
            <div class="mt-2">
              <label class="inline-flex items-center">
                <input
                  type="checkbox"
                  id="unknownTime"
                  name="unknownTime"
                  class="form-checkbox h-5 w-5 text-blue-600"
                />
                <span class="ml-2 text-gray-700"
                  >I don't know the time of birth</span
                >
              </label>
            </div>
            <div class="mt-6">
              <button
                type="submit"
                id="cal-btn"
                class="w-full bg-blue-600 text-white font-semibold py-3 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-150 ease-in-out"
              >
                Calculate Sign
              </button>
            </div>
          </form>
        </div>

        <div
          id="result-container"
          class="w-full p-4 mt-4 rounded-md"
          style="
            box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
              rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
          "
        >
          <h1 id="result-heading" class="text-gray-900 text-sm"></h1>
          <p id="result-sign" class="text-xl text-gray-900"></p>
          <hr/>
          <div >
            <h1 class="text-gray-900 text-lg font-bold" style="margin: 25px 0px !important;">
              Your Other Signs are:
            </h1>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-5">
              <div
                class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
                style="
                  box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                    rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
                "
              >
                <img src="<?php echo plugins_url('assets/sun.jpg', __FILE__); ?>" alt="" class="w-14" />
                <h3 class="text-2xl text-gray-900" id="result-sun"></h3>
              </div>

              <div
                class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
                style="
                  box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                    rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
                "
              >
                <img src="<?php echo plugins_url('assets/moon.jpg', __FILE__); ?>" alt="" class="w-14" />
                <h3 class="text-2xl text-gray-900" id="result-moon"></h3>
              </div>

              <div
                class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
                style="
                  box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                    rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
                "
              >
                <img src="<?php echo plugins_url('assets/mercury.jpg', __FILE__); ?>" alt="" class="w-14" />
                <h3 class="text-2xl text-gray-900" id="result-mercury"></h3>
              </div>

              <div
                class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
                style="
                  box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                    rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
                "
              >
                <img src="<?php echo plugins_url('assets/venus.jpg', __FILE__); ?>" alt="" class="w-14" />
                <h3 class="text-2xl text-gray-900" id="result-venus"></h3>
              </div>

              <div
                class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
                style="
                  box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                    rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
                "
              >
                <img src="<?php echo plugins_url('assets/mars.jpg', __FILE__); ?>" alt="" class="w-14" />
                <h3 class="text-2xl text-gray-900" id="result-mars"></h3>
              </div>

              <div
                class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
                style="
                  box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                    rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
                "
              >
                <img src="<?php echo plugins_url('assets/jupiter.jpg', __FILE__); ?>" alt="" class="w-14" />
                <h3 class="text-2xl text-gray-900" id="result-jupiter"></h3>
              </div>

              <div
                class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
                style="
                  box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                    rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
                "
              >
                <img src="<?php echo plugins_url('assets/saturn.jpg', __FILE__); ?>" alt="" class="w-14" />
                <h3 class="text-2xl text-gray-900" id="result-saturn"></h3>
              </div>

              <div
                class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
                style="
                  box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                    rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
                "
              >
                <img src="<?php echo plugins_url('assets/uranus.jpg', __FILE__); ?>" alt="" class="w-14" />
                <h3 class="text-2xl text-gray-900" id="result-uranus"></h3>
              </div>

              <div
                class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
                style="
                  box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                    rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
                "
              >
                <img src="<?php echo plugins_url('assets/neptune.jpg', __FILE__); ?>" alt="" class="w-14" />
                <h3 class="text-2xl text-gray-900" id="result-neptune"></h3>
              </div>

              <div
                class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
                style="
                  box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                    rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
                "
              >
                <img src="<?php echo plugins_url('assets/pluto.jpg', __FILE__); ?>" alt="" class="w-14" />
                <h3 class="text-2xl text-gray-900" id="result-pluto"></h3>
              </div>

              <div
                class="rounded-md flex justify-center items-center flex-col p-4 cursor-pointer"
                style="
                  box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px,
                    rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
                "
              >
                <img src="/<?php echo plugins_url('assets/asc.jpg', __FILE__); ?>" alt="" class="w-14" />
                <h3 class="text-2xl text-gray-900" id="result-asc"></h3>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <?php
    return ob_get_clean();
}

// Register shortcode
function register_astrology_calculator_shortcode() {
    add_shortcode('astrology_calculator', 'astrology_calculator_shortcode');
}
add_action('init', 'register_astrology_calculator_shortcode');