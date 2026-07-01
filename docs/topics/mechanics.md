---
layout: default
title: Topic - mechanics
---


# mechanics

<article class="paper">
<h2>An analytical self-consistent theory for the elastic moduli of granular materials</h2>
<p class="meta"><strong>Authors:</strong> Ge Duan, Chaofa Zhao, Zhongxuan Yang</p>
<p class="meta"><strong>Date:</strong> 2026-09-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 215 - Article 106733</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106733</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>

<p>An accurate prediction of the effective elastic moduli from contact-scale properties is essential for multiscale constitutive modelling of granular materials. In the derivation of the moduli from microscopic characteristics, it is crucial that the localisation operator, which expresses relative displacements at contacts in terms of macroscopic deformation, satisfies the kinematic consistency condition. This study develops a self-consistent pair-fluctuation (SC-PF) theory to predict the elastic moduli of two-dimensional isotropic granular assemblies of disk-shaped particles. The theory incorporates an explicitly enforced kinematic consistency condition, leading to a localisation operator that produces relative displacements consistent with the prescribed macroscopic strain, and consequently improved elastic moduli. The proposed SC-PF theory is evaluated using two-dimensional Discrete Element Method (DEM) simulations performed under isotropic compression and pure shear loading. Owing to its enforcement of self-consistency, the SC-PF theory provides substantially improved predictions of both the displacement fluctuations and elastic moduli, across a range of coordination numbers and contact stiffness ratios. In particular, the SC-PF theory improves the prediction of the bulk and shear moduli, with relative deviations reduced by 69% and 65%, respectively, compared with the mean-field theory, and by 22% and 45% compared with the pair-fluctuation approach of Jenkins et al. (2005). Beyond improved accuracy, the SC-PF theory provides insight into how the geometric and mechanical characteristics of interparticle contacts govern macroscopic elastic behaviour, thereby advancing multiscale constitutive modelling of granular materials.</p>
<p><a href="https://doi.org/10.1016/j.jmps.2026.106733">Publisher Link</a></p>
<section class="ai-notes">
<h3>AI Notes</h3>
<p><strong>文章做了什么：</strong>文章针对二维各向同性圆盘颗粒组，发展了一种自洽对波动理论，用于从接触尺度特性（如接触刚度、配位数）预测其宏观有效弹性模量（体积模量与剪切模量）。核心任务是构建一个满足运动学一致性条件的局部化算子，以改进现有微观力学理论的预测精度。</p>
<p><strong>为什么做：</strong>从微观特性准确预测宏观弹性模量是颗粒材料多尺度本构建模的关键。现有理论（如平均场理论和Jenkins等人的对波动方法）在构建局部化算子时，未能严格满足运动学一致性条件，即接触点的相对位移与宏观应变之间的一致性关系，这限制了弹性模量预测的准确性。</p>
<p><strong>怎么做：</strong>1. 理论模型：在经典对波动方法框架内，引入自洽概念，为参考接触的邻近接触赋予待定的自洽接触刚度。通过显式地强制执行运动学一致性条件，推导出改进的局部化算子，进而得到宏观弹性模量的解析表达式。2. 验证方法：通过二维离散元法模拟，在等向压缩和纯剪切加载路径下生成不同配位数和接触刚度比的颗粒组，将理论预测的位移波动和弹性模量与DEM结果进行对比，并与平均场理论及Jenkins等人的对波动方法进行定量比较。</p>
<p><strong>做得怎么样：</strong>理论验证效果显著。相比平均场理论，SC-PF理论对体积模量和剪切模量预测的相对偏差分别降低了69%和65%；相比Jenkins等人的对波动方法，分别降低了22%和45%。该理论在一系列配位数和接触刚度比范围内，对位移波动和弹性模量的预测均有实质性改进。</p>
<h4>主要结论</h4>
<ul><li>提出的自洽对波动理论显著提高了对二维颗粒材料弹性模量的预测精度。</li>
<li>在局部化算子中显式强制执行运动学一致性条件是提升预测准确性的关键。</li>
<li>该理论揭示了颗粒间接触的几何与力学特性（通过配位数和接触刚度比）如何控制宏观弹性行为，为多尺度本构建模提供了更可靠的微观力学基础。</li></ul>
<h4>亮点和创新点</h4>
<ul><li>将对波动方法与自洽概念相结合，提出了SC-PF理论，在保证解析性的同时显著提升了精度。</li>
<li>明确地将运动学一致性条件作为约束引入理论推导，修正了局部化算子。</li>
<li>提供了对微观位移波动与宏观弹性响应之间关联的更深入理解，超越了单纯的经验拟合。</li></ul>
<h4>局限性</h4>
<ul><li>理论目前仅适用于二维、各向同性、由圆盘颗粒组成的组构，且假设了线性弹性接触和稳态接触网络。</li>
<li>未考虑颗粒自身旋转、有限变形以及接触滑移或脱离等非线性行为。</li></ul>
<h4>可能的发展方向</h4>
<ul><li>将理论框架扩展到三维颗粒体系及非球形颗粒。</li>
<li>纳入颗粒旋转、非线性接触律（如Hertz-Mindlin）以及塑性滑移，以描述更广泛的力学行为。</li>
<li>探索将该微观力学框架应用于复杂加载路径下的本构模型开发。</li></ul>
<h4>注意事项</h4>
<ul><li>该理论预测的是小应变下的弹性响应，不直接适用于大变形或塑性流动阶段。</li>
<li>理论中所需的参数（如配位数、接触分布）通常依赖于DEM模拟或实验统计，其获取方式可能影响预测的普适性。</li>
<li>与更复杂的数值均匀化方法相比，该解析理论基于一系列简化假设，在极端微观结构下可能存在偏差。</li></ul>
<p><strong>关键词：</strong>弹性模量, 颗粒材料, 自洽理论, 多尺度建模, 离散元法</p>
<p><strong>适合读者：</strong>从事颗粒物质力学、岩土工程多尺度本构建模、材料微观力学研究的科研人员。</p>
<p><strong>阅读优先级：</strong>high。该工作在经典颗粒材料微观力学理论（平均场、对波动）基础上做出了明确且显著的改进，提出了一个兼具理论严谨性和预测精度的新模型，并给出了详尽的定量验证。对于关注颗粒材料弹性预测和多尺度方法的研究者而言，这是一篇近期发表在JMPS上的重要文献。</p>
</section>
</article>

<article class="paper">
<h2>A parametric study of slow dynamic nonlinear elasticity with comparisons to models</h2>
<p class="meta"><strong>Authors:</strong> Richard L. Weaver, John Y. Yoritomo</p>
<p class="meta"><strong>Date:</strong> 2026-09-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 215 - Article 106727</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106727</p>
<p class="meta"><strong>Keywords:</strong> elasticity</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>

<p>Several phenomenological models that aspire to quantitative description of anomalous nonlinear mesoscopic elasticity are reviewed and compared with laboratory measurements. This class of nonlinearity, best known perhaps for slow dynamics and aging, is seen widely in imperfectly consolidated granular solids but is not well understood. Typical slow dynamic tests show that a modest conditioning oscillatory &quot;pump&quot; strain depresses material stiffness, which then recovers like the logarithm of time after conditioning ceases. Several phenomenological models based on physical arguments have been proposed that predict the material stiffness response to arbitrary pump strain histories during conditioning and recovery. Approximate closed form and numerical solutions to the models are presented that predict the quantitative influence of three key pump parameters: the pump&#x27;s strain amplitude, the pump&#x27;s strain rate, and the pump’s duration. Laboratory measurements on Berea sandstone, concrete and a confined single aluminum bead find that slow dynamic responses are linear in pump strain and independent of pump frequency. Measurements also show that, after pump-off, stiffness recovers over times far longer than the pump duration. These observations and others are compared to model predictions. One of the considered models, based on a picture of fast brittle damage and slow healing, successfully matches all these behaviors.</p>
<p><a href="https://doi.org/10.1016/j.jmps.2026.106727">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Classification of rotational zero modes in 2D micropolar solids</h2>
<p class="meta"><strong>Authors:</strong> Dingxin Sun, Yi Chen, Gengkai Hu</p>
<p class="meta"><strong>Date:</strong> 2026-09-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 215 - Article 106704</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106704</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>

<p>Zero modes, which are deformations that cost zero energy, underlie many exotic behaviors in elastic metamaterials. While classical linear Cauchy elasticity explains many of these modes, those linked to the rotations of metamaterial inner components often lie beyond its scope. Micropolar elasticity, which incorporates translation and rotation degrees of freedom, provides a framework for capturing these rotational modes. Herein, we present the first complete symmetry-based classification of zero modes in two-dimensional micropolar solids, with an emphasis on rotation-related modes. Guided by this classification, we construct threefold rotationally symmetric micropolar metamaterials and realize typical rotational micropolar zero modes. We further show that these metamaterials exhibit wave phenomena forbidden in Cauchy continua, including the emergence of three bulk waves in the long-wavelength limit and associated triple refraction, chiral acoustic modes, as well as strong wave anisotropy. All intriguing properties are quantitatively captured by micropolar continuum descriptions, whereas the classical Cauchy continuum theory fails to predict these behaviors, even at a qualitative level. Our results establish a general framework for engineering rotation-based zero modes, opening avenues for designing metamaterials with novel wave properties.</p>
<p><a href="https://doi.org/10.1016/j.jmps.2026.106704">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Graph-field framework for fracture mechanics of architected lattice materials</h2>
<p class="meta"><strong>Authors:</strong> Yang Gao, Junjie Liu, Xiaoding Wei</p>
<p class="meta"><strong>Date:</strong> 2026-09-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 215 - Article 106729</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106729</p>
<p class="meta"><strong>Keywords:</strong> architected, fracture, lattice, mechanics</p>
<p class="meta"><strong>Topics:</strong> fracture, mechanics, metamaterials</p>

<p>Fracture in architected lattice materials challenges classical Linear Elastic Fracture Mechanics (LEFM) due to the breakdown of scale separation and the dominance of discrete topological effects. This study establishes a rigorous Graph-Field (GF) framework that bridges discrete topology and continuum theory by mapping nodal equilibrium directly to partial differential equations via a vanishing-cell-size limit. Unlike phenomenological homogenization, the GF approach explicitly captures architecture-induced anomalous couplings and non-affine kinematics without empirical fitting. We reveal that distinct topological hierarchies (i.e., single-level versus dual-level architectures) and internal kinematic constraints fundamentally reshape near-tip kinematic fields, generating unconventional deformation patterns missed by standard orthotropic models. Furthermore, a parameter-free criterion based on maximum principal strain is shown to accurately predict kinked crack trajectories, by identifying the physical “weakest link” within the network. Finally, using Eshelby’s configurational mechanics, we derive a path-independent crack driving force. This metric reveals that standard ASTM fracture testing protocols intrinsically smooth out localized kinematics and can severely overestimate the toughness of highly constrained, dual-level lattices. Ultimately, the GF framework provides a thermodynamically consistent foundation for the experimental characterization, generative inverse design, and broad multi-scale exploration of complex structural metamaterials.</p>
<p><a href="https://doi.org/10.1016/j.jmps.2026.106729">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Fabric evolution modeling for granular materials under various monotonic and cyclic stress paths accounting for nonproportionality</h2>
<p class="meta"><strong>Authors:</strong> Rui Wang, Weibin Mo, Qi Liu, Jian-Min Zhang, Yannis F. Dafalias</p>
<p class="meta"><strong>Date:</strong> 2026-09-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 215 - Article 106728</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106728</p>
<p class="meta"><strong>Keywords:</strong> stress</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2026.106728">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Unifying mean-field models through the method of multiscale virtual power and its dual formulation</h2>
<p class="meta"><strong>Authors:</strong> José L.P. Vila-Chã, António M. Couto Carneiro, Bernardo P. Ferreira, F.M. Andrade Pires</p>
<p class="meta"><strong>Date:</strong> 2026-09-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 215 - Article 106724</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106724</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2026.106724">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Predicting slip transmission in polycrystalline Ni</h2>
<p class="meta"><strong>Authors:</strong> Rembert D. White, Yang Su, Josh Kacher, Irene J. Beyerlein</p>
<p class="meta"><strong>Date:</strong> 2026-09-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 215 - Article 106726</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106726</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2026.106726">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Polydisperse polymer networks with irregular topologies: Mechanics of cross-link distributions</h2>
<p class="meta"><strong>Authors:</strong> Jason Mulderrig, Michael Buche, Matthew Grasinger</p>
<p class="meta"><strong>Date:</strong> 2026-09-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 215 - Article 106706</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106706</p>
<p class="meta"><strong>Keywords:</strong> mechanics</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2026.106706">Publisher Link</a></p>

</article>

<article class="paper">
<h2>A constitutive framework for distortional-mode-dependent failure in soft materials: Tension–compression asymmetry and beyond</h2>
<p class="meta"><strong>Authors:</strong> Yogesh C. Chandrashekar, Kshitiz Upadhyay</p>
<p class="meta"><strong>Date:</strong> 2026-09-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 215 - Article 106700</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106700</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2026.106700">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Temperature and strain-rate dependence of plasticity in a TiZrHf refractory multi-principal element alloy: Microscopic mechanism and constitutive modeling</h2>
<p class="meta"><strong>Authors:</strong> Xiaying Ma, Kerong Ren, Peiyuan Ma, Houcheng Xu, Zhijun Zheng, Zhibin Li, Shun Li, Hang Wang, Zihan Zhang, Rong Chen</p>
<p class="meta"><strong>Date:</strong> 2026-09-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 215 - Article 106722</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106722</p>
<p class="meta"><strong>Keywords:</strong> plastic, plasticity, strain</p>
<p class="meta"><strong>Topics:</strong> mechanics, plasticity</p>


<p><a href="https://doi.org/10.1016/j.jmps.2026.106722">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Bulk and surface control of micro-displacements</h2>
<p class="meta"><strong>Authors:</strong> G. Zurlo, L. Truskinovsky</p>
<p class="meta"><strong>Date:</strong> 2026-09-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 215 - Article 106737</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106737</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2026.106737">Publisher Link</a></p>

</article>

<article class="paper">
<h2>A predictive stochastic continuum framework for concrete subjected to high-velocity impact loading</h2>
<p class="meta"><strong>Authors:</strong> Sohanjit Ghosh, Michael A. Homel, Zhifei Deng, Ryan C. Hurley</p>
<p class="meta"><strong>Date:</strong> 2026-09-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 215 - Article 106716</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106716</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2026.106716">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Roles of lattice distortion and chemical short-range order in dislocation drag and strain-rate sensitivity over wide strain rates</h2>
<p class="meta"><strong>Authors:</strong> Guanyu Huang, Xiaoqing Zhang, Xuetao Zou, Kai Wang, Zhuocheng Xie, Wu-Rong Jian, Shuang Qin, Xiaohu Yao</p>
<p class="meta"><strong>Date:</strong> 2026-09-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 215 - Article 106723</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106723</p>
<p class="meta"><strong>Keywords:</strong> dislocation, lattice, strain</p>
<p class="meta"><strong>Topics:</strong> dislocations, mechanics, metamaterials</p>


<p><a href="https://doi.org/10.1016/j.jmps.2026.106723">Publisher Link</a></p>

</article>

<article class="paper">
<h2>The Mullins effect, mechanical preconditioning, and predictive power</h2>
<p class="meta"><strong>Authors:</strong> Maximilian P. Wollner, Gerhard A. Holzapfel</p>
<p class="meta"><strong>Date:</strong> 2026-09-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 215 - Article 106698</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106698</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2026.106698">Publisher Link</a></p>

</article>

<article class="paper">
<h2>On asymptotic-stress-amplitude-driven phase field modeling of crack growth in a hyperelastic continuum</h2>
<p class="meta"><strong>Authors:</strong> Xuan Hu, Shaofan Li</p>
<p class="meta"><strong>Date:</strong> 2026-09-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 215 - Article 106695</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106695</p>
<p class="meta"><strong>Keywords:</strong> crack, phase field, stress</p>
<p class="meta"><strong>Topics:</strong> fracture, mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2026.106695">Publisher Link</a></p>

</article>

<article class="paper">
<h2>High strain rate behavior of liquid crystal elastomers</h2>
<p class="meta"><strong>Authors:</strong> Adeline Wihardja, Juan Carlos Nieto-Fuentes, Daniel Rittel, Kaushik Bhattacharya</p>
<p class="meta"><strong>Date:</strong> 2026-03-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 209 - Article 106501</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106501</p>
<p class="meta"><strong>Keywords:</strong> elastomer, strain</p>
<p class="meta"><strong>Topics:</strong> mechanics, soft matter</p>


<p><a href="https://doi.org/10.1016/j.jmps.2026.106501">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Editorial Board</h2>
<p class="meta"><strong>Authors:</strong> Unknown authors</p>
<p class="meta"><strong>Date:</strong> 2026-03-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 209 - Article 106537</p>
<p class="meta"><strong>DOI:</strong> 10.1016/s0022-5096(26)00037-2</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/s0022-5096(26)00037-2">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Electro-mechanical wrinkling of soft dielectric films bonded to hyperelastic substrates</h2>
<p class="meta"><strong>Authors:</strong> Bin Wu, Linghao Kong, Weiqiu Chen, Davide Riccobelli, Michel Destrade</p>
<p class="meta"><strong>Date:</strong> 2026-03-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 209 - Article 106490</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106490</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106490">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Shear banding in high-entropy alloy</h2>
<p class="meta"><strong>Authors:</strong> De-Ru Wang, Tong Li, Ming-Yao Su, Yan Chen, Hai-Ying Wang, Lan-Hong Dai</p>
<p class="meta"><strong>Date:</strong> 2026-03-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 209 - Article 106517</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106517</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2026.106517">Publisher Link</a></p>

</article>

<article class="paper">
<h2>A stationary phase-based theory of diffraction: Modeling three-dimensional elastic wave diffraction from defect edges with arbitrary shapes</h2>
<p class="meta"><strong>Authors:</strong> Zhengyu Wei, Fan Shi</p>
<p class="meta"><strong>Date:</strong> 2026-03-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 209 - Article 106498</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106498</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106498">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Modeling axisymmetric contact problems within strain gradient elasticity</h2>
<p class="meta"><strong>Authors:</strong> Lucca Schek, Aleksandr Morozov, Sergei Khakalo, Wolfgang H. Müller</p>
<p class="meta"><strong>Date:</strong> 2026-03-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 209 - Article 106513</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106513</p>
<p class="meta"><strong>Keywords:</strong> elasticity, strain</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2026.106513">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Experimentally reconstructing the interplay of slip and microstructure in polycrystalline shape-memory alloys</h2>
<p class="meta"><strong>Authors:</strong> Andrew Christison, Harshad M. Paranjape, Samantha Daly</p>
<p class="meta"><strong>Date:</strong> 2026-03-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 209 - Article 106518</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106518</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2026.106518">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Nonadditive quantum friction at water-carbon interfaces on substrates</h2>
<p class="meta"><strong>Authors:</strong> Zonghuiyi Jiang, Zhuhua Zhang, Zepu Kou, Yuquan Zhou, Fangyuan Chen, Jun Yin, Wanlin Guo, Xiaofei Liu</p>
<p class="meta"><strong>Date:</strong> 2026-03-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 209 - Article 106522</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106522</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2026.106522">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Capturing the fractocohesive length scale in elastomers through a statistical mechanics-based gradient enhanced damage model</h2>
<p class="meta"><strong>Authors:</strong> S. Mohammad Mousavi, Jason Mulderrig, Brandon Talamini, Nikolaos Bouklas</p>
<p class="meta"><strong>Date:</strong> 2026-03-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 209 - Article 106504</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106504</p>
<p class="meta"><strong>Keywords:</strong> damage, elastomer, mechanics</p>
<p class="meta"><strong>Topics:</strong> fracture, mechanics, soft matter</p>


<p><a href="https://doi.org/10.1016/j.jmps.2026.106504">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Mechanics of sequential damage in twisted fiber bundles across scales</h2>
<p class="meta"><strong>Authors:</strong> Siqi Yan, Xizhe Zhang, Zhaoxin Zhang, Zheng Jia, Shuze Zhu</p>
<p class="meta"><strong>Date:</strong> 2026-03-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 209 - Article 106516</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2026.106516</p>
<p class="meta"><strong>Keywords:</strong> damage, mechanics</p>
<p class="meta"><strong>Topics:</strong> fracture, mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2026.106516">Publisher Link</a></p>

</article>

<article class="paper">
<h2>In search of constitutive conditions in isotropic hyperelasticity: polyconvexity versus true-stress-true-strain monotonicity</h2>
<p class="meta"><strong>Authors:</strong> Maximilian P. Wollner, Gerhard A. Holzapfel, Patrizio Neff</p>
<p class="meta"><strong>Date:</strong> 2026-03-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 209 - Article 106465</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106465</p>
<p class="meta"><strong>Keywords:</strong> elasticity, strain, stress</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106465">Publisher Link</a></p>

</article>

<article class="paper">
<h2>A probabilistic buckling model for hemispherical shells with non-interacting localized defects</h2>
<p class="meta"><strong>Authors:</strong> Zheren Baizhikova, Uba K. Ubamanyu, Fani Derveni, Roberto Ballarini, Pedro M. Reis, Jia-Liang Le</p>
<p class="meta"><strong>Date:</strong> 2026-02-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 208 - Article 106468</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106468</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106468">Publisher Link</a></p>

</article>

<article class="paper">
<h2>The broad wrinkling landscape of hyperelastic parallelogram-shaped membranes: From wrinkle migration to restabilization and their subsequent reappearance elsewhere</h2>
<p class="meta"><strong>Authors:</strong> Mohammad Hosein Nejabatmeimandi, Francesco Dal Corso</p>
<p class="meta"><strong>Date:</strong> 2026-02-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 208 - Article 106461</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106461</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106461">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Editorial Board</h2>
<p class="meta"><strong>Authors:</strong> Unknown authors</p>
<p class="meta"><strong>Date:</strong> 2026-02-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 208 - Article 106508</p>
<p class="meta"><strong>DOI:</strong> 10.1016/s0022-5096(26)00008-6</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/s0022-5096(26)00008-6">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Coupled thermo-chemo-mechanical modeling of reactive solids: Applications to thermochemical energy storage materials</h2>
<p class="meta"><strong>Authors:</strong> Srivatsa Bhat Kaudur, Claudio V. Di Leo</p>
<p class="meta"><strong>Date:</strong> 2026-02-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 208 - Article 106448</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106448</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106448">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Do discrete fine-scale mechanical models with rotational degrees of freedom homogenize into a Cosserat or a Cauchy continuum?</h2>
<p class="meta"><strong>Authors:</strong> Jan Eliáš, Gianluca Cusatis</p>
<p class="meta"><strong>Date:</strong> 2026-02-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 207 - Article 106422</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106422</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106422">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Interfacial evolution explains the complex swelling-shrinkage responses of porous materials from vacuum-dry to full liquid saturation</h2>
<p class="meta"><strong>Authors:</strong> Mohammadali Behboodi, Yida Zhang</p>
<p class="meta"><strong>Date:</strong> 2026-02-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 207 - Article 106425</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106425</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106425">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Continuum theory for the mechanics of curved epithelial shells by coarse-graining an ensemble of active gel cellular surfaces</h2>
<p class="meta"><strong>Authors:</strong> Pradeep K. Bal, Adam Ouzeri, Marino Arroyo</p>
<p class="meta"><strong>Date:</strong> 2026-02-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 208 - Article 106477</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106477</p>
<p class="meta"><strong>Keywords:</strong> gel, mechanics</p>
<p class="meta"><strong>Topics:</strong> mechanics, soft matter</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106477">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Indentation-based anisotropic material parameter identifiability: Validation on a synthetic soft tissue phantom</h2>
<p class="meta"><strong>Authors:</strong> Amit Ashkenazi, Adi Shultz, Lee Jordan, Dana Solav</p>
<p class="meta"><strong>Date:</strong> 2026-02-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 208 - Article 106417</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106417</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106417">Publisher Link</a></p>

</article>

<article class="paper">
<h2>TPMS sheet structures with orthorhombic symmetry: Anisotropic elasticity and energy absorption</h2>
<p class="meta"><strong>Authors:</strong> Stephen Daynes</p>
<p class="meta"><strong>Date:</strong> 2026-02-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 208 - Article 106489</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106489</p>
<p class="meta"><strong>Keywords:</strong> elasticity</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106489">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Wrinkling mechanics of immersed magneto-active hydrogels</h2>
<p class="meta"><strong>Authors:</strong> Guozhan Xia, Renwei Mao, Weiqiu Chen, Yipin Su</p>
<p class="meta"><strong>Date:</strong> 2026-02-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 208 - Article 106430</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106430</p>
<p class="meta"><strong>Keywords:</strong> gel, hydrogel, mechanics</p>
<p class="meta"><strong>Topics:</strong> mechanics, soft matter</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106430">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Using a negative exponent to prevent unphysical instability in fiber-reinforced hyperelastic materials</h2>
<p class="meta"><strong>Authors:</strong> Hio Konishi, Seishiro Matsubara, So Nagashima, Dai Okumura</p>
<p class="meta"><strong>Date:</strong> 2026-02-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 208 - Article 106480</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106480</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106480">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Material Fingerprinting for rapid discovery of hyperelastic models: First experimental validation</h2>
<p class="meta"><strong>Authors:</strong> Denisa Martonová, Ellen Kuhl, Moritz Flaschel</p>
<p class="meta"><strong>Date:</strong> 2026-02-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 208 - Article 106463</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106463</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106463">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Micromechanical insights into the uniaxial stress-strain behaviour of glassy amorphous polymers through molecular dynamics simulations</h2>
<p class="meta"><strong>Authors:</strong> Pramod Kumar Patel, Sumit Basu</p>
<p class="meta"><strong>Date:</strong> 2026-02-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 208 - Article 106496</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106496</p>
<p class="meta"><strong>Keywords:</strong> simulation, strain, stress</p>
<p class="meta"><strong>Topics:</strong> computational mechanics, mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106496">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Modeling coupled electro-chemo-mechanical phenomena within all-solid-state battery composite cathodes</h2>
<p class="meta"><strong>Authors:</strong> Kasra Taghikhani, William Huber, Peter J. Weddle, Mohsen Asle Zaeem, J.R. Berger, Robert J. Kee</p>
<p class="meta"><strong>Date:</strong> 2025-05-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 198 - Article 106060</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106060</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106060">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Torsion-mediated instabilities in confined elastic layers</h2>
<p class="meta"><strong>Authors:</strong> Tara K. Venkatadri, Chuwei Ye, Tal Cohen, Shaoting Lin</p>
<p class="meta"><strong>Date:</strong> 2025-05-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 198 - Article 106064</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106064</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106064">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Phase-augmented digital image correlation for high-accuracy deformation measurement: Theory, validation, and application to constitutive law learning</h2>
<p class="meta"><strong>Authors:</strong> Rahul Danda, Xinxin Wu, Sheng Mao, Yin Zhang, Ting Zhu, Shuman Xia</p>
<p class="meta"><strong>Date:</strong> 2025-05-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 198 - Article 106051</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106051</p>
<p class="meta"><strong>Keywords:</strong> deformation</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106051">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Editorial Board</h2>
<p class="meta"><strong>Authors:</strong> Unknown authors</p>
<p class="meta"><strong>Date:</strong> 2025-05-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 198 - Article 106094</p>
<p class="meta"><strong>DOI:</strong> 10.1016/s0022-5096(25)00070-5</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/s0022-5096(25)00070-5">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Analysis of axisymmetric necking of a circular dielectric membrane based on a one-dimensional model</h2>
<p class="meta"><strong>Authors:</strong> Xiang Yu, Yibin Fu</p>
<p class="meta"><strong>Date:</strong> 2025-05-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 198 - Article 106071</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106071</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106071">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Editorial Board</h2>
<p class="meta"><strong>Authors:</strong> Unknown authors</p>
<p class="meta"><strong>Date:</strong> 2025-04-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 197 - Article 106083</p>
<p class="meta"><strong>DOI:</strong> 10.1016/s0022-5096(25)00059-6</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/s0022-5096(25)00059-6">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Magnetothermal dehydration induced deformation of hydrogel structures: Modelling and experiment</h2>
<p class="meta"><strong>Authors:</strong> Jingda Tang, Huangsan Wei, Wenjie Zhang, Jiayi Lin, Chao Yuan, Tiejun Wang</p>
<p class="meta"><strong>Date:</strong> 2025-04-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 197 - Article 106061</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106061</p>
<p class="meta"><strong>Keywords:</strong> deformation, gel, hydrogel</p>
<p class="meta"><strong>Topics:</strong> mechanics, soft matter</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106061">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Mechanics of liquid crystal inclusions in soft matrices</h2>
<p class="meta"><strong>Authors:</strong> Yifei Bai, Laurence Brassart</p>
<p class="meta"><strong>Date:</strong> 2025-04-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 197 - Article 106070</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106070</p>
<p class="meta"><strong>Keywords:</strong> mechanics</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106070">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Synergistic toughening mechanisms of macro- and micro-structures in nacre: Effects of T-stresses</h2>
<p class="meta"><strong>Authors:</strong> Yi Yan, Xi-Qiao Feng</p>
<p class="meta"><strong>Date:</strong> 2025-04-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 197 - Article 106067</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106067</p>
<p class="meta"><strong>Keywords:</strong> stress</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106067">Publisher Link</a></p>

</article>

<article class="paper">
<h2>A unified morphomechanics theory framework for both Euclidean and non-Euclidean curved crease origami</h2>
<p class="meta"><strong>Authors:</strong> Yinzheng Yu, Ruoman Zhu, Kai Wei, Xujing Yang</p>
<p class="meta"><strong>Date:</strong> 2025-04-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 197 - Article 106046</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106046</p>
<p class="meta"><strong>Keywords:</strong> mechanics</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106046">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Parthenocissus tricuspidata tendril: A mechanically robust structural design with multiple functions</h2>
<p class="meta"><strong>Authors:</strong> Jin-Hui Zhou, Lin Zhang, Sen-Zhen Zhan, Qiao Zhang, Yuxin Sun, Xi-Qiao Feng, Zi-Long Zhao</p>
<p class="meta"><strong>Date:</strong> 2025-04-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 197 - Article 106065</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106065</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106065">Publisher Link</a></p>

</article>

<article class="paper">
<h2>t-PiNet: A thermodynamics-informed hierarchical learning for discovering constitutive relations of geomaterials</h2>
<p class="meta"><strong>Authors:</strong> Pin Zhang, Konstantinos Karapiperis, Oliver Weeger</p>
<p class="meta"><strong>Date:</strong> 2025-04-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 197 - Article 106049</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106049</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106049">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Indentation on a constrained electroactive gel</h2>
<p class="meta"><strong>Authors:</strong> Guozhan Xia</p>
<p class="meta"><strong>Date:</strong> 2025-04-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 197 - Article 106045</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106045</p>
<p class="meta"><strong>Keywords:</strong> gel, strain</p>
<p class="meta"><strong>Topics:</strong> mechanics, soft matter</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106045">Publisher Link</a></p>

</article>

<article class="paper">
<h2>The deformation mode transition of indented elastic thin shell induced by localized curvature imperfection</h2>
<p class="meta"><strong>Authors:</strong> Chongxi Jiao, Xinming Qiu</p>
<p class="meta"><strong>Date:</strong> 2025-04-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 197 - Article 106039</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106039</p>
<p class="meta"><strong>Keywords:</strong> deformation</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106039">Publisher Link</a></p>

</article>

<article class="paper">
<h2>A chemo-thermo-mechanically coupled theory of photo-reacting polymers: Application to modeling photo-degradation with irradiation-driven heat transfer</h2>
<p class="meta"><strong>Authors:</strong> Keven Alkhoury, Shawn A. Chester</p>
<p class="meta"><strong>Date:</strong> 2025-04-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 197 - Article 106050</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2025.106050</p>
<p class="meta"><strong>Keywords:</strong> None</p>
<p class="meta"><strong>Topics:</strong> mechanics</p>


<p><a href="https://doi.org/10.1016/j.jmps.2025.106050">Publisher Link</a></p>

</article>

<article class="paper">
<h2>Phase field fracture in elastoplastic solids: a stress-state, strain-rate, and orientation dependent model in explicit dynamics and its applications to additively manufactured metals</h2>
<p class="meta"><strong>Authors:</strong> Cunyi Li, Jian Liu, Le Dong, Chi Wu, Grant Steven, Qing Li, Jianguang Fang</p>
<p class="meta"><strong>Date:</strong> 2025-04-01</p>
<p class="meta"><strong>Journal:</strong> Journal of the Mechanics and Physics of Solids - Volume 197 - Article 105978</p>
<p class="meta"><strong>DOI:</strong> 10.1016/j.jmps.2024.105978</p>
<p class="meta"><strong>Keywords:</strong> fracture, phase field, plastic, strain, stress</p>
<p class="meta"><strong>Topics:</strong> fracture, mechanics, plasticity</p>


<p><a href="https://doi.org/10.1016/j.jmps.2024.105978">Publisher Link</a></p>

</article>
