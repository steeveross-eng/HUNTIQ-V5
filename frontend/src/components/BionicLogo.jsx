/**
 * BionicLogo - Composant Logo Global V5-ULTIME-FUSION
 * 
 * Deux modes d'utilisation:
 * 1. Logo fixe global (position fixed, coin supérieur gauche)
 * 2. Logo inline pour header/navigation
 * 
 * Dimensions: ~2.5cm x 2.5cm (96px x 96px à 96dpi)
 */

import React from 'react';
import { Link } from 'react-router-dom';

// Logo fixe global - visible sur toutes les pages
export const BionicLogoGlobal = ({ 
  size = 96,  // ~2.5cm à 96dpi
  className = ''
}) => {
  return (
    <Link 
      to="/"
      className={`
        fixed
        top-20 left-4
        z-30
        transition-all duration-300
        hover:scale-105
        hover:drop-shadow-[0_0_15px_rgba(245,166,35,0.5)]
        hidden lg:block
        ${className}
      `}
      data-testid="bionic-logo-global"
      aria-label="BIONIC - Retour à l'accueil"
    >
      <img 
        src="/logos/bionic-logo-official.png"
        alt="BIONIC Chasse / Hunt"
        width={size}
        height={size}
        className="object-contain drop-shadow-lg rounded-xl"
        style={{
          width: `${size}px`,
          height: `${size}px`,
          minWidth: `${size}px`,
          minHeight: `${size}px`
        }}
      />
    </Link>
  );
};

// Logo inline pour header/navigation
const BionicLogo = ({ 
  className = '',
  size = 'default' // 'default', 'small', 'large'
}) => {
  const sizeClasses = {
    small: 'h-6 w-6',
    default: 'h-8 w-8',
    large: 'h-10 w-10'
  };

  return (
    <img 
      src="/logos/bionic-logo-official.png"
      alt="BIONIC"
      className={`object-contain ${sizeClasses[size] || sizeClasses.default} ${className}`}
      data-testid="bionic-logo-inline"
    />
  );
};

export default BionicLogo;
