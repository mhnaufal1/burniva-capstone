import {
  ClipboardCheck,
  Brain,
  Lightbulb,
  ListTodo,
  LineChart,
  LayoutDashboard,
  ArrowRight,
  CheckCircle2,
  Circle,
} from "lucide-react";

function FeaturesSection() {
  return (
    <section
      id="fitur"
      className="py-14 md:py-24 bg-white relative overflow-hidden"
    >
      <div className="w-full px-4 md:px-16 lg:px-24 relative z-10">
        <div className="text-center mb-12 md:mb-16 max-w-3xl mx-auto">
          <p className="inline-block bg-primary-100 text-primary-600 text-xs md:text-sm font-medium px-3 py-1 rounded-full mb-4">
            Fitur
          </p>
          <h2 className="text-2xl md:text-4xl font-bold text-slate-800 mb-4 leading-tight">
            Semua yang Kamu Butuhkan untuk
            <br className="hidden md:block" /> Menjaga Kesehatan Mental
          </h2>
          <p className="text-sm md:text-base text-slate-500 leading-relaxed">
            Burniva menghadirkan fitur yang dirancang khusus untuk membantu
            mahasiswa memahami kondisi mental dan mencegah burnout secara lebih
            dini.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
          {/* Card 1: Daily Mental Check-in */}
          <div className="bg-white rounded-[24px] md:rounded-[32px] p-6 md:p-8 border border-slate-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgb(0,0,0,0.08)] hover:-translate-y-1.5 transition-all duration-300 group flex flex-col cursor-default">
            <div className="w-10 h-10 rounded-xl bg-primary-50 flex items-center justify-center text-primary-600 mb-4 group-hover:scale-110 group-hover:bg-primary-600 group-hover:text-white transition-all duration-300">
              <ClipboardCheck size={20} />
            </div>
            <h3 className="text-base font-semibold text-slate-800 mb-1">
              Daily Mental Check-in
            </h3>
            <p className="text-xs text-slate-500 leading-relaxed mb-6">
              Check-in harian sederhana hanya dalam beberapa menit untuk
              memahami kondisi mentalmu hari ini.
            </p>
            <div className="mt-auto flex flex-col gap-3">
              <div className="bg-slate-50 border border-slate-100 rounded-xl p-4 flex justify-between items-center group-hover:border-primary-100 transition-colors">
                <span className="text-xs sm:text-sm text-slate-500">
                  Bagaimana mood-mu hari ini?
                </span>
                <ArrowRight
                  size={16}
                  className="text-primary-400 group-hover:translate-x-1 transition-transform"
                />
              </div>
              <div className="bg-slate-50 border border-slate-100 rounded-xl p-4 flex justify-between items-center group-hover:border-primary-100 transition-colors delay-75">
                <span className="text-xs sm:text-sm text-slate-500">
                  Kualitas tidur semalam?
                </span>
                <ArrowRight
                  size={16}
                  className="text-primary-400 group-hover:translate-x-1 transition-transform"
                />
              </div>
            </div>
          </div>

          {/* Card 2: AI Burnout Detection */}
          <div className="bg-white rounded-[24px] md:rounded-[32px] p-6 md:p-8 border border-slate-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgb(0,0,0,0.08)] hover:-translate-y-1.5 transition-all duration-300 group flex flex-col cursor-default">
            <div className="w-10 h-10 rounded-xl bg-primary-50 flex items-center justify-center text-primary-600 mb-4 group-hover:scale-110 group-hover:bg-primary-600 group-hover:text-white transition-all duration-300">
              <Brain size={20} />
            </div>
            <h3 className="text-base font-semibold text-slate-800 mb-1">
              AI Burnout Detection
            </h3>
            <p className="text-xs text-slate-500 leading-relaxed mb-6">
              AI menganalisis pola aktivitas, stres, dan kondisi mental untuk
              mendeteksi risiko burnout secara lebih akurat.
            </p>
            <div className="mt-auto bg-slate-50 border border-slate-100 rounded-xl p-5 flex items-end justify-between h-28 gap-1.5 overflow-hidden relative">
              <div className="w-full bg-primary-600/20 rounded-t-sm h-[20%] group-hover:h-[30%] transition-all duration-500"></div>
              <div className="w-full bg-primary-600/40 rounded-t-sm h-[30%] group-hover:h-[45%] transition-all duration-500 delay-75"></div>
              <div className="w-full bg-primary-600/60 rounded-t-sm h-[25%] group-hover:h-[40%] transition-all duration-500 delay-100"></div>
              <div className="w-full bg-primary-600/80 rounded-t-sm h-[40%] group-hover:h-[60%] transition-all duration-500 delay-150"></div>
              <div className="w-full bg-primary-600 rounded-t-sm h-[35%] group-hover:h-[50%] transition-all duration-500 delay-200"></div>
              <div className="w-full bg-primary-700 rounded-t-sm h-[50%] group-hover:h-[80%] transition-all duration-500 delay-300"></div>
              <div className="w-full bg-primary-800 rounded-t-sm h-[45%] group-hover:h-[60%] transition-all duration-500 delay-200"></div>
            </div>
          </div>

          {/* Card 3: Personalized AI Insight */}
          <div className="bg-white rounded-[24px] md:rounded-[32px] p-6 md:p-8 border border-slate-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgb(0,0,0,0.08)] hover:-translate-y-1.5 transition-all duration-300 group flex flex-col cursor-default">
            <div className="w-10 h-10 rounded-xl bg-primary-50 flex items-center justify-center text-primary-600 mb-4 group-hover:scale-110 group-hover:bg-primary-600 group-hover:text-white transition-all duration-300">
              <Lightbulb size={20} />
            </div>
            <h3 className="text-base font-semibold text-slate-800 mb-1">
              Personalized AI Insight
            </h3>
            <p className="text-xs text-slate-500 leading-relaxed mb-6">
              Dapatkan insight personal yang mudah dipahami berdasarkan hasil
              kondisi mental harianmu.
            </p>
            <div className="mt-auto bg-slate-50 border border-slate-100 rounded-xl p-5 relative group-hover:border-primary-100 transition-colors">
              <div className="absolute -left-1 -top-3 text-4xl text-primary-200 font-serif leading-none opacity-0 group-hover:opacity-100 group-hover:-top-5 transition-all duration-300">
                "
              </div>
              <p className="text-xs sm:text-sm text-slate-500 italic leading-relaxed z-10 relative">
                "Kamu menunjukkan tanda kelelahan akademik. Pertimbangkan
                istirahat mental hari ini."
              </p>
            </div>
          </div>

          {/* Card 4: Smart Recovery To-Do */}
          <div className="bg-white rounded-[24px] md:rounded-[32px] p-6 md:p-8 border border-slate-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgb(0,0,0,0.08)] hover:-translate-y-1.5 transition-all duration-300 group flex flex-col cursor-default">
            <div className="w-10 h-10 rounded-xl bg-primary-50 flex items-center justify-center text-primary-600 mb-4 group-hover:scale-110 group-hover:bg-primary-600 group-hover:text-white transition-all duration-300">
              <ListTodo size={20} />
            </div>
            <h3 className="text-base font-semibold text-slate-800 mb-1">
              Smart Recovery To-Do
            </h3>
            <p className="text-xs text-slate-500 leading-relaxed mb-6">
              Burniva secara otomatis membuat rekomendasi aktivitas harian
              berbasis AI untuk membantu proses pemulihan mental.
            </p>
            <div className="mt-auto bg-slate-50 border border-slate-100 rounded-xl p-5 flex flex-col gap-3.5">
              <div className="flex items-center gap-2.5 text-xs sm:text-sm text-slate-500">
                <CheckCircle2
                  size={16}
                  className="text-primary-500 shrink-0 group-hover:scale-110 transition-transform"
                />
                <span className="line-through text-slate-400">
                  Tidur lebih awal
                </span>
              </div>
              <div className="flex items-center gap-2.5 text-xs sm:text-sm text-slate-500">
                <Circle
                  size={16}
                  className="text-slate-300 shrink-0 group-hover:text-primary-400 transition-colors delay-75"
                />
                <span>Jalan kaki 15 menit</span>
              </div>
              <div className="flex items-center gap-2.5 text-xs sm:text-sm text-slate-500">
                <Circle
                  size={16}
                  className="text-slate-300 shrink-0 group-hover:text-primary-400 transition-colors delay-100"
                />
                <span>Kurangi screen time</span>
              </div>
            </div>
          </div>

          {/* Card 5: Progress Tracking */}
          <div className="bg-white rounded-[24px] md:rounded-[32px] p-6 md:p-8 border border-slate-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgb(0,0,0,0.08)] hover:-translate-y-1.5 transition-all duration-300 group flex flex-col cursor-default">
            <div className="w-10 h-10 rounded-xl bg-primary-50 flex items-center justify-center text-primary-600 mb-4 group-hover:scale-110 group-hover:bg-primary-600 group-hover:text-white transition-all duration-300">
              <LineChart size={20} />
            </div>
            <h3 className="text-base font-semibold text-slate-800 mb-1">
              Progress Tracking
            </h3>
            <p className="text-xs text-slate-500 leading-relaxed mb-6">
              Pantau perkembangan kondisi mentalmu dari waktu ke waktu melalui
              riwayat dan tren aktivitas.
            </p>
            <div className="mt-auto bg-slate-50 border border-slate-100 rounded-xl h-28 relative overflow-hidden group-hover:border-primary-200 transition-colors">
              {/* Header Mini Chart */}
              <div className="absolute top-3 left-4 right-4 flex justify-between items-center z-10">
                <span className="text-[11px] font-semibold text-slate-500">
                  Tren 7 Hari
                </span>
                <span className="text-[10px] font-bold px-2 py-1 rounded flex items-center gap-1 bg-emerald-100 text-emerald-700 leading-none">
                  {/* Ikon TrendingDown (Karna risiko menurun = membaik) */}
                  <svg
                    className="w-3 h-3"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="3"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <polyline points="22 17 13.5 8.5 8.5 13.5 2 7"></polyline>
                    <polyline points="16 17 22 17 22 11"></polyline>
                  </svg>
                  Membaik
                </span>
              </div>

              {/* Area Grafik SVG */}
              <div className="absolute inset-x-0 bottom-2 top-9 flex justify-center">
                <svg
                  className="w-[90%] h-full overflow-visible"
                  viewBox="0 0 300 80"
                >
                  {/* Background Gradient Area */}
                  <path
                    d="M 10,65 L 10,15 C 40,15 70,30 100,30 C 150,30 150,25 200,25 C 250,25 250,55 290,55 L 290,65 Z"
                    fill="url(#trend-gradient-final)"
                    className="opacity-0 group-hover:opacity-100 transition-opacity duration-700 delay-300"
                  />

                  {/* Garis Dasar Statis */}
                  <path
                    d="M 10,15 C 40,15 70,30 100,30 C 150,30 150,25 200,25 C 250,25 250,55 290,55"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="4"
                    strokeLinecap="round"
                    className="text-slate-200"
                  />

                  {/* Garis Utama Animasi Tumbuh */}
                  <path
                    d="M 10,15 C 40,15 70,30 100,30 C 150,30 150,25 200,25 C 250,25 250,55 290,55"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="4"
                    strokeLinecap="round"
                    className="text-primary-600 [stroke-dasharray:350] [stroke-dashoffset:350] group-hover:[stroke-dashoffset:0] transition-all duration-[1200ms] ease-out"
                  />

                  {/* Titik-titik Data */}
                  <g className="text-primary-600 fill-white stroke-current stroke-[3px] opacity-0 group-hover:opacity-100 transition-opacity duration-500 delay-[800ms]">
                    <circle cx="10" cy="15" r="3.5" />
                    <circle cx="100" cy="30" r="3.5" />
                    <circle cx="200" cy="25" r="3.5" />
                    {/* Titik Terakhir (Highlight) */}
                    <circle
                      cx="290"
                      cy="55"
                      r="5"
                      className="fill-primary-600 text-white"
                    />
                  </g>

                  {/* Label Sumbu X di dalam SVG agar posisinya terkunci */}
                  <g
                    className="fill-slate-400 text-[11px] font-medium"
                    style={{ fontFamily: "inherit" }}
                  >
                    <text x="10" y="80" textAnchor="start">
                      Sen
                    </text>
                    <text x="150" y="80" textAnchor="middle">
                      Rab
                    </text>
                    <text x="290" y="80" textAnchor="end">
                      Min
                    </text>
                  </g>

                  {/* Definisi Gradient */}
                  <defs>
                    <linearGradient
                      id="trend-gradient-final"
                      x1="0"
                      x2="0"
                      y1="0"
                      y2="1"
                    >
                      <stop
                        offset="0%"
                        stopColor="#14532d"
                        stopOpacity="0.12"
                      />
                      <stop offset="100%" stopColor="#14532d" stopOpacity="0" />
                    </linearGradient>
                  </defs>
                </svg>
              </div>
            </div>
          </div>

          {/* Card 6: Admin Monitoring Dashboard */}
          <div className="bg-white rounded-[24px] md:rounded-[32px] p-6 md:p-8 border border-slate-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgb(0,0,0,0.08)] hover:-translate-y-1.5 transition-all duration-300 group flex flex-col cursor-default">
            <div className="w-10 h-10 rounded-xl bg-primary-50 flex items-center justify-center text-primary-600 mb-4 group-hover:scale-110 group-hover:bg-primary-600 group-hover:text-white transition-all duration-300">
              <LayoutDashboard size={20} />
            </div>
            <h3 className="text-base font-semibold text-slate-800 mb-1">
              Admin Monitoring Dashboard
            </h3>
            <p className="text-xs text-slate-500 leading-relaxed mb-6">
              Pantau tren burnout pengguna melalui dashboard monitoring untuk
              kebutuhan evaluasi dan analitik.
            </p>
            <div className="mt-auto flex items-center gap-3">
              <div className="flex-1 bg-slate-50 border border-slate-100 rounded-lg p-3.5 flex flex-col gap-2 group-hover:-translate-y-1 transition-transform duration-300">
                <div className="w-6 h-1.5 rounded-full bg-primary-600"></div>
                <div className="w-full h-1 rounded-full bg-slate-200"></div>
                <div className="w-3/4 h-1 rounded-full bg-slate-200"></div>
              </div>
              <div className="flex-1 bg-slate-50 border border-slate-100 rounded-lg p-3.5 flex flex-col gap-2 group-hover:-translate-y-2 transition-transform duration-300 delay-75">
                <div className="w-6 h-1.5 rounded-full bg-emerald-500"></div>
                <div className="w-full h-1 rounded-full bg-slate-200"></div>
                <div className="w-3/4 h-1 rounded-full bg-slate-200"></div>
              </div>
              <div className="flex-1 bg-slate-50 border border-slate-100 rounded-lg p-3.5 flex flex-col gap-2 group-hover:-translate-y-1 transition-transform duration-300 delay-150">
                <div className="w-6 h-1.5 rounded-full bg-amber-500"></div>
                <div className="w-full h-1 rounded-full bg-slate-200"></div>
                <div className="w-3/4 h-1 rounded-full bg-slate-200"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default FeaturesSection;
