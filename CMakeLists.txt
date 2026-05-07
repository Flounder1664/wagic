# CMakeLists.txt — Linux SDL build of Wagic.
#
# Targets x86_64 Linux (including Steam Deck / SteamOS). Mirrors the Windows
# MSVC source set in projects/mtg/template.vcxproj + JGE/JGE.vcxproj, but
# compiled for native Linux against system SDL 1.2, OpenGL, zlib, and Boost.
#
# Build:
#     mkdir build-linux && cd build-linux
#     cmake -DCMAKE_BUILD_TYPE=Release ..
#     make -j$(nproc)
#
# Output: build-linux/wagic ELF binary.
#
# Run:
#     cd projects/mtg/bin && ../../../build-linux/wagic
# (cwd must contain Res/ — the AppImage launcher does this automatically.)

cmake_minimum_required(VERSION 3.10)
project(wagic CXX C)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# ---- Dependencies ----------------------------------------------------------

find_package(PkgConfig REQUIRED)
# SDLmain.cpp uses a mix of SDL 1.2 (SDL_SetVideoMode) and SDL2-only
# (SDL_Window, SDL_TouchFingerEvent) APIs because Wagic ships against the
# bundled SDL 1.3 transitional version. On Linux we have neither — only
# system SDL2 — so the `#if defined(LINUX) && !defined(ANDROID)` blocks in
# SDLmain.cpp use the SDL2 idiom (CreateWindow + GL_CreateContext +
# GL_SwapWindow + SetWindowTitle).
pkg_check_modules(SDL2 REQUIRED sdl2)
find_package(OpenGL REQUIRED)
find_package(ZLIB REQUIRED)
find_package(Threads REQUIRED)
find_package(Boost REQUIRED COMPONENTS system thread)
find_package(X11 REQUIRED)        # TranslateKeys.cpp uses XKeysymToString
find_package(PNG REQUIRED)        # JGfx.cpp PNG decoding
find_package(JPEG REQUIRED)       # JGfx.cpp JPEG decoding

# giflib — JRenderer.h includes <gif_lib.h>; link with -lgif.
find_path(GIF_INCLUDE_DIR gif_lib.h)
find_library(GIF_LIBRARY NAMES gif)
if(NOT GIF_INCLUDE_DIR OR NOT GIF_LIBRARY)
    message(FATAL_ERROR "giflib not found — install libgif-dev")
endif()

# freetype2 — JTTFont.h includes <ft2build.h>.
pkg_check_modules(FREETYPE REQUIRED freetype2)

# ---- Compiler flags --------------------------------------------------------

add_compile_options(
    -Wall -Wno-unused -Wno-unused-parameter
    -Wno-unused-but-set-variable -Wno-unused-but-set-parameter
    -Wno-unused-value -Wno-unused-local-typedefs
    -Wno-nonnull-compare
    -fpermissive
)

add_definitions(
    -DLINUX
    -DNETWORK_SUPPORT
    -DTIXML_USE_STL
    -DRESPATH=\"Res\"
)

include_directories(
    JGE/include
    JGE/src/zipFS
    Boost
    projects/mtg/include
    ${SDL2_INCLUDE_DIRS}
    ${GIF_INCLUDE_DIR}
    ${FREETYPE_INCLUDE_DIRS}
)

# ---- MTG game sources (mirrors projects/mtg/template.vcxproj) --------------

set(MTG_SRC_DIR projects/mtg/src)
file(GLOB MTG_SOURCES
    "${MTG_SRC_DIR}/AbilityParser.cpp"
    "${MTG_SRC_DIR}/ActionElement.cpp"
    "${MTG_SRC_DIR}/ActionLayer.cpp"
    "${MTG_SRC_DIR}/ActionStack.cpp"
    "${MTG_SRC_DIR}/AIHints.cpp"
    "${MTG_SRC_DIR}/AIMomirPlayer.cpp"
    "${MTG_SRC_DIR}/AIPlayer.cpp"
    "${MTG_SRC_DIR}/AIPlayerBaka.cpp"
    "${MTG_SRC_DIR}/AIPlayerBakaB.cpp"
    "${MTG_SRC_DIR}/AIStats.cpp"
    "${MTG_SRC_DIR}/AllAbilities.cpp"
    "${MTG_SRC_DIR}/CardDescriptor.cpp"
    "${MTG_SRC_DIR}/CardDisplay.cpp"
    "${MTG_SRC_DIR}/CardGui.cpp"
    "${MTG_SRC_DIR}/CardPrimitive.cpp"
    "${MTG_SRC_DIR}/CardSelector.cpp"
    "${MTG_SRC_DIR}/CardSelectorSingleton.cpp"
    "${MTG_SRC_DIR}/CarouselDeckView.cpp"
    "${MTG_SRC_DIR}/Closest.cpp"
    "${MTG_SRC_DIR}/Counters.cpp"
    "${MTG_SRC_DIR}/Credits.cpp"
    "${MTG_SRC_DIR}/Damage.cpp"
    "${MTG_SRC_DIR}/DamagerDamaged.cpp"
    "${MTG_SRC_DIR}/DeckDataWrapper.cpp"
    "${MTG_SRC_DIR}/DeckEditorMenu.cpp"
    "${MTG_SRC_DIR}/DeckManager.cpp"
    "${MTG_SRC_DIR}/DeckMenu.cpp"
    "${MTG_SRC_DIR}/DeckMenuItem.cpp"
    "${MTG_SRC_DIR}/DeckMetaData.cpp"
    "${MTG_SRC_DIR}/DeckStats.cpp"
    "${MTG_SRC_DIR}/DeckView.cpp"
    "${MTG_SRC_DIR}/DuelLayers.cpp"
    "${MTG_SRC_DIR}/ExtraCost.cpp"
    "${MTG_SRC_DIR}/GameApp.cpp"
    "${MTG_SRC_DIR}/GameLauncher.cpp"
    "${MTG_SRC_DIR}/GameObserver.cpp"
    "${MTG_SRC_DIR}/GameOptions.cpp"
    "${MTG_SRC_DIR}/GameState.cpp"
    "${MTG_SRC_DIR}/GameStateAwards.cpp"
    "${MTG_SRC_DIR}/GameStateDeckViewer.cpp"
    "${MTG_SRC_DIR}/GameStateDuel.cpp"
    "${MTG_SRC_DIR}/GameStateMenu.cpp"
    "${MTG_SRC_DIR}/GameStateOptions.cpp"
    "${MTG_SRC_DIR}/GameStateShop.cpp"
    "${MTG_SRC_DIR}/GameStateStory.cpp"
    "${MTG_SRC_DIR}/GameStateTransitions.cpp"
    "${MTG_SRC_DIR}/GridDeckView.cpp"
    "${MTG_SRC_DIR}/GuiAvatars.cpp"
    "${MTG_SRC_DIR}/GuiBackground.cpp"
    "${MTG_SRC_DIR}/GuiCardsController.cpp"
    "${MTG_SRC_DIR}/GuiCombat.cpp"
    "${MTG_SRC_DIR}/GuiFrame.cpp"
    "${MTG_SRC_DIR}/GuiHand.cpp"
    "${MTG_SRC_DIR}/GuiLayers.cpp"
    "${MTG_SRC_DIR}/GuiMana.cpp"
    "${MTG_SRC_DIR}/GuiPhaseBar.cpp"
    "${MTG_SRC_DIR}/GuiPlay.cpp"
    "${MTG_SRC_DIR}/GuiStatic.cpp"
    "${MTG_SRC_DIR}/IconButton.cpp"
    "${MTG_SRC_DIR}/InteractiveButton.cpp"
    "${MTG_SRC_DIR}/ManaCost.cpp"
    "${MTG_SRC_DIR}/ManaCostHybrid.cpp"
    "${MTG_SRC_DIR}/MenuItem.cpp"
    "${MTG_SRC_DIR}/ModRules.cpp"
    "${MTG_SRC_DIR}/MTGAbility.cpp"
    "${MTG_SRC_DIR}/MTGCard.cpp"
    "${MTG_SRC_DIR}/MTGCardInstance.cpp"
    "${MTG_SRC_DIR}/MTGDeck.cpp"
    "${MTG_SRC_DIR}/MTGDefinitions.cpp"
    "${MTG_SRC_DIR}/MTGGamePhase.cpp"
    "${MTG_SRC_DIR}/MTGGameZones.cpp"
    "${MTG_SRC_DIR}/MTGPack.cpp"
    "${MTG_SRC_DIR}/MTGRules.cpp"
    "${MTG_SRC_DIR}/ObjectAnalytics.cpp"
    "${MTG_SRC_DIR}/OptionItem.cpp"
    "${MTG_SRC_DIR}/PhaseRing.cpp"
    "${MTG_SRC_DIR}/PlayGuiObject.cpp"
    "${MTG_SRC_DIR}/PlayGuiObjectController.cpp"
    "${MTG_SRC_DIR}/PlayRestrictions.cpp"
    "${MTG_SRC_DIR}/Player.cpp"
    "${MTG_SRC_DIR}/PlayerData.cpp"
    "${MTG_SRC_DIR}/Pos.cpp"
    "${MTG_SRC_DIR}/PriceList.cpp"
    "${MTG_SRC_DIR}/ReplacementEffects.cpp"
    "${MTG_SRC_DIR}/Rules.cpp"
    "${MTG_SRC_DIR}/SimpleButton.cpp"
    "${MTG_SRC_DIR}/SimpleMenu.cpp"
    "${MTG_SRC_DIR}/SimpleMenuItem.cpp"
    "${MTG_SRC_DIR}/SimplePad.cpp"
    "${MTG_SRC_DIR}/SimplePopup.cpp"
    "${MTG_SRC_DIR}/StoryFlow.cpp"
    "${MTG_SRC_DIR}/StyleManager.cpp"
    "${MTG_SRC_DIR}/Subtypes.cpp"
    "${MTG_SRC_DIR}/TargetChooser.cpp"
    "${MTG_SRC_DIR}/TargetsList.cpp"
    "${MTG_SRC_DIR}/Tasks.cpp"
    "${MTG_SRC_DIR}/TestSuiteAI.cpp"
    "${MTG_SRC_DIR}/TextScroller.cpp"
    "${MTG_SRC_DIR}/ThisDescriptor.cpp"
    "${MTG_SRC_DIR}/Token.cpp"
    "${MTG_SRC_DIR}/Translate.cpp"
    "${MTG_SRC_DIR}/TranslateKeys.cpp"
    "${MTG_SRC_DIR}/Trash.cpp"
    "${MTG_SRC_DIR}/utils.cpp"
    "${MTG_SRC_DIR}/WCachedResource.cpp"
    "${MTG_SRC_DIR}/WDataSrc.cpp"
    "${MTG_SRC_DIR}/WEvent.cpp"
    "${MTG_SRC_DIR}/WFilter.cpp"
    "${MTG_SRC_DIR}/WFont.cpp"
    "${MTG_SRC_DIR}/WGui.cpp"
    "${MTG_SRC_DIR}/WParsedInt.cpp"
    "${MTG_SRC_DIR}/WResourceManager.cpp"
)

# ---- JGE engine sources (mirrors JGE/JGE.vcxproj) --------------------------

set(JGE_SOURCES
    # NOTE: JGE/src/Downloader.cpp is Qt-only (QNetworkReply etc.) — not built here.
    JGE/src/Encoding.cpp
    JGE/src/JAnimator.cpp
    JGE/src/JApp.cpp
    JGE/src/JDistortionMesh.cpp
    JGE/src/JFileSystem.cpp
    JGE/src/JGBKFont.cpp
    JGE/src/JGE.cpp
    JGE/src/JGameObject.cpp
    JGE/src/JGui.cpp
    JGE/src/JLBFont.cpp
    JGE/src/JLogger.cpp
    JGE/src/JMD2Model.cpp
    JGE/src/JNetwork.cpp
    JGE/src/JOBJModel.cpp
    JGE/src/JParticle.cpp
    JGE/src/JParticleEffect.cpp
    JGE/src/JParticleEmitter.cpp
    JGE/src/JParticleSystem.cpp
    JGE/src/JResourceManager.cpp
    JGE/src/JSpline.cpp
    JGE/src/JSprite.cpp
    JGE/src/JTTFont.cpp
    JGE/src/SDLmain.cpp
    JGE/src/Vector2D.cpp
    JGE/src/hge/hgecolor.cpp
    JGE/src/hge/hgedistort.cpp
    JGE/src/hge/hgefont.cpp
    JGE/src/hge/hgeparticle.cpp
    JGE/src/hge/hgepmanager.cpp
    JGE/src/hge/hgerect.cpp
    JGE/src/hge/hgevector.cpp
    JGE/src/pc/JGfx.cpp
    JGE/src/pc/JSfx.cpp
    JGE/src/pc/JSocket.cpp
    JGE/src/tinyxml/tinystr.cpp
    JGE/src/tinyxml/tinyxml.cpp
    JGE/src/tinyxml/tinyxmlerror.cpp
    JGE/src/tinyxml/tinyxmlparser.cpp
    JGE/src/zipFS/zfsystem.cpp
    JGE/src/zipFS/ziphdr.cpp
    JGE/src/zipFS/zstream.cpp
)

# ---- Target ----------------------------------------------------------------

add_executable(wagic ${MTG_SOURCES} ${JGE_SOURCES})

target_link_libraries(wagic PRIVATE
    ${SDL2_LIBRARIES}
    OpenGL::GL
    OpenGL::GLU
    ZLIB::ZLIB
    ${GIF_LIBRARY}
    ${FREETYPE_LIBRARIES}
    ${X11_LIBRARIES}
    PNG::PNG
    JPEG::JPEG
    Boost::system
    Boost::thread
    Threads::Threads
    dl
)

target_link_directories(wagic PRIVATE ${SDL2_LIBRARY_DIRS} ${FREETYPE_LIBRARY_DIRS})

# Copy executable into projects/mtg/bin so it can find Res/ for ad-hoc runs.
add_custom_command(TARGET wagic POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
        $<TARGET_FILE:wagic>
        ${CMAKE_SOURCE_DIR}/projects/mtg/bin/wagic
)
