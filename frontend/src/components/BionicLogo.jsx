/**
 * BionicLogo - Composant Logo Global V5-ULTIME-FUSION
 * 
 * DIRECTIVES:
 * - PAGE PRINCIPALE: logo 2.2x (211px)
 * - AUTRES PAGES: logo taille normale (96px)
 * - TOUTES PAGES: transparent, sans carré, sans fond
 * - Position: coin supérieur gauche, sous header
 */

import React from 'react';
import { Link, useLocation } from 'react-router-dom';

// Logo global fixe - Taille variable selon la page
export const BionicLogoGlobal = () => {
  const location = useLocation();
  const isHomePage = location.pathname === '/' || location.pathname === '';
  
  // Taille: 211px sur page principale, 96px ailleurs
  const logoSize = isHomePage ? 211 : 96;
  
  return (
    <Link 
      to="/"
      style={{
        position: 'fixed',
        top: '80px',
        left: '16px',
        zIndex: 50,
        width: `${logoSize}px`,
        height: `${logoSize}px`,
        display: 'block',
        background: 'transparent'
      }}
      data-testid="bionic-logo-global"
      aria-label="BIONIC - Retour à l'accueil"
    >
      <img 
        src="/logos/bionic-logo-official.png"
        alt="BIONIC Chasse / Hunt"
        style={{
          width: `${logoSize}px`,
          height: `${logoSize}px`,
          objectFit: 'contain',
          mixBlendMode: 'lighten'
        }}
      />
    </Link>
  );
};

// Logo inline (non utilisé)
const BionicLogo = ({ className = '' }) => {
  return (
    <img 
      src="/logos/bionic-logo-official.png"
      alt="BIONIC"
      className={className}
      style={{ 
        width: '32px', 
        height: '32px',
        objectFit: 'contain',
        mixBlendMode: 'lighten'
      }}
    />
  );
};

export default BionicLogo;
